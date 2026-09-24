import test from "node:test";
import assert from "node:assert/strict";

/**
 * Story 2 & Story 7: Frontend stale result protection and parameter schema defaults.
 */

// Model of the monotonic sequence guard used in metricsStore
class MockMetricsRunner {
  currentSequence = 0;
  activeFocusNodeId: string | null = null;
  activeResult: any = null;

  async execute(focusNodeId: string | null, delayMs: number, resultPayload: any): Promise<void> {
    const seq = ++this.currentSequence;
    this.activeFocusNodeId = focusNodeId;

    await new Promise((resolve) => setTimeout(resolve, delayMs));

    // Stale result rejection guard: discard if sequence or focus node changed
    if (seq !== this.currentSequence) {
      return; // Silently discard out-of-order response
    }
    if (focusNodeId && this.activeFocusNodeId !== focusNodeId) {
      return; // Silently discard mismatching focus node response
    }

    this.activeResult = resultPayload;
  }
}

test("stale result protection: slower request A is ignored when fast request B completes", async () => {
  const runner = new MockMetricsRunner();

  // Trigger request A (slow: 50ms)
  const taskA = runner.execute("node_A", 50, { node: "node_A", value: 0.1 });

  // Rapidly switch to node B (fast: 10ms)
  const taskB = runner.execute("node_B", 10, { node: "node_B", value: 0.9 });

  await Promise.all([taskA, taskB]);

  // Ensure result for node B was kept and node A was discarded
  assert.equal(runner.activeResult?.node, "node_B");
  assert.equal(runner.activeResult?.value, 0.9);
});

test("stale result protection: focus node change discards unresolved execution", async () => {
  const runner = new MockMetricsRunner();

  const taskA = runner.execute("node_A", 20, { node: "node_A", value: 0.5 });
  // User switches focus node before A finishes
  runner.activeFocusNodeId = "node_C";

  await taskA;
  assert.equal(runner.activeResult, null);
});

// Dynamic form parameter extraction helper
function extractFormDefaults(paramSchema: Record<string, any>): Record<string, any> {
  const defaults: Record<string, any> = {};
  if (!paramSchema || !paramSchema.properties) return defaults;

  for (const [key, spec] of Object.entries<any>(paramSchema.properties)) {
    if (spec.default !== undefined) {
      defaults[key] = spec.default;
    } else if (spec.type === "boolean") {
      defaults[key] = false;
    } else if (spec.type === "integer" || spec.type === "number") {
      defaults[key] = 0;
    } else if (spec.type === "string") {
      defaults[key] = "";
    }
  }
  return defaults;
}

test("dynamic form defaults extractor correctly initializes schema defaults", () => {
  const schema = {
    type: "object",
    properties: {
      max_depth: { type: "integer", default: 2 },
      tolerance: { type: "number", default: 0.0001 },
      enabled: { type: "boolean", default: true },
      unspecified_bool: { type: "boolean" },
      unspecified_num: { type: "number" },
      title: { type: "string" },
    },
  };

  const defaults = extractFormDefaults(schema);
  assert.equal(defaults.max_depth, 2);
  assert.equal(defaults.tolerance, 0.0001);
  assert.equal(defaults.enabled, true);
  assert.equal(defaults.unspecified_bool, false);
  assert.equal(defaults.unspecified_num, 0);
  assert.equal(defaults.title, "");
});

test("metrics pane tab filter correctly partitions local and global descriptors", () => {
  const mockDescriptors = [
    { id: "gradual_strength_local", scope: "single_node" },
    { id: "pagerank_global", scope: "global" },
    { id: "degree_global", scope: "global" },
    { id: "component_global", scope: "global" },
  ];

  const filterByTab = (tab: "local" | "global" | "all") => {
    if (tab === "local") return mockDescriptors.filter((d) => d.scope === "single_node");
    if (tab === "global") return mockDescriptors.filter((d) => d.scope === "global");
    return mockDescriptors;
  };

  assert.equal(filterByTab("local").length, 1);
  assert.equal(filterByTab("local")[0].id, "gradual_strength_local");

  assert.equal(filterByTab("global").length, 3);
  assert.deepEqual(
    filterByTab("global").map((d) => d.id),
    ["pagerank_global", "degree_global", "component_global"]
  );

  assert.equal(filterByTab("all").length, 4);
});

test("edge inspector correctly extracts neo4j properties and filters embedding", () => {
  const mockEdge = {
    id: "edge_42",
    source: "claim_1",
    target: "claim_2",
    type: "SUPPORTS",
    layer: 3,
    polarity: 1,
    weight: 0.85,
    confidence: 0.92,
    props: {
      similarity: 0.88,
      source_sentence: "Kant argues that synthetic a priori judgments are possible.",
      embedding: [0.12, 0.34, 0.56],
      schema_layer: "L3",
    },
  };

  const propEntries = Object.entries(mockEdge.props || {}).filter(([k]) => k !== "embedding");
  assert.equal(propEntries.length, 3);
  assert.equal(propEntries.find(([k]) => k === "similarity")?.[1], 0.88);
  assert.equal(propEntries.find(([k]) => k === "embedding"), undefined);
});

test("computeStyleConflicts correctly identifies size and color collisions", async () => {
  const { computeStyleConflicts } = await import("../store/metricsStore.ts");

  const mockInstances: any[] = [
    {
      instanceId: "inst_1",
      metricId: "pagerank_global",
      status: "completed",
      result: { affected_nodes: {} },
      styling: { enabled: true, sizeScaling: true, colorGradient: true },
    },
    {
      instanceId: "inst_2",
      metricId: "degree_global",
      status: "completed",
      result: { affected_nodes: {} },
      styling: { enabled: true, sizeScaling: true, colorGradient: false },
    },
    {
      instanceId: "inst_3",
      metricId: "leiden_global",
      status: "completed",
      result: { affected_nodes: {} },
      styling: { enabled: true, sizeScaling: false, colorGradient: true },
    },
  ];

  const conflicts = computeStyleConflicts(mockInstances);
  assert.equal(conflicts.hasSizeConflict, true, "Should detect 2 size scaling algorithms");
  assert.equal(conflicts.activeSizeCount, 2);
  assert.deepEqual(conflicts.conflictingSizeInstances, ["inst_1", "inst_2"]);

  assert.equal(conflicts.hasColorConflict, true, "Should detect 2 color gradient algorithms");
  assert.equal(conflicts.activeColorCount, 2);
  assert.deepEqual(conflicts.conflictingColorInstances, ["inst_1", "inst_3"]);
});

test("computeNodeStyle handles multi-metric size stacking vs overwrite mode", async () => {
  const { computeNodeStyle } = await import("../graph/styling/nodeStyling.ts");

  const node: any = {
    id: "n1",
    layer: 3,
    type: "TheoryAtom",
    label: "Synthetic a priori",
    synthetic: false,
    resolved: true,
  };

  const baseSettings: any = {
    nodeSizeMultiplier: 1.0,
    edgeThicknessMultiplier: 1.0,
    labelFontSize: 11,
    labelMaxLength: 24,
  };

  const inst1: any = {
    instanceId: "i1",
    metricId: "pagerank_global",
    status: "completed",
    result: {
      metric_id: "pagerank_global",
      affected_nodes: {
        n1: { roles: ["centrality"], metadata: { pagerank: 0.8 } },
      },
    },
    styling: { enabled: true, sizeScaling: true, colorGradient: false },
  };

  const inst2: any = {
    instanceId: "i2",
    metricId: "degree_global",
    status: "completed",
    result: {
      metric_id: "degree_global",
      affected_nodes: {
        n1: { roles: ["centrality"], metadata: { degree: 0.8 } },
      },
    },
    styling: { enabled: true, sizeScaling: true, colorGradient: false },
  };

  // 1. Stack mode: sizes compound
  const styleStack = computeNodeStyle(node, {
    isDark: true,
    activeOverlay: null,
    activeMetricResult: null,
    metricInstances: [inst1, inst2],
    scaleMode: "stack",
    isDiffActive: false,
    diffData: null,
    graphSettings: baseSettings,
    getPartition: () => null,
  });

  // 2. Overwrite mode: only top metric applies
  const styleOverwrite = computeNodeStyle(node, {
    isDark: true,
    activeOverlay: null,
    activeMetricResult: null,
    metricInstances: [inst1, inst2],
    scaleMode: "overwrite",
    isDiffActive: false,
    diffData: null,
    graphSettings: baseSettings,
    getPartition: () => null,
  });

  assert.ok(
    styleStack.size > styleOverwrite.size,
    `Stack size (${styleStack.size}) should compound larger than overwrite size (${styleOverwrite.size})`
  );
});

test("computeNodeStyle modulates node size based on sizeStrength influence (subtle, normal, strong)", async () => {
  const { computeNodeStyle } = await import("../graph/styling/nodeStyling.ts");

  const node: any = {
    id: "n1",
    layer: 3,
    type: "TheoryAtom",
    label: "Synthetic a priori",
    synthetic: false,
    resolved: true,
  };

  const baseSettings: any = {
    nodeSizeMultiplier: 1.0,
    edgeThicknessMultiplier: 1.0,
    labelFontSize: 11,
    labelMaxLength: 24,
  };

  const createInstance = (sizeStrength: "subtle" | "normal" | "strong"): any => ({
    instanceId: `inst_${sizeStrength}`,
    metricId: "pagerank_global",
    status: "completed",
    result: {
      metric_id: "pagerank_global",
      affected_nodes: {
        n1: { roles: ["centrality"], metadata: { pagerank: 0.8 } },
      },
    },
    styling: { enabled: true, sizeScaling: true, colorGradient: false, sizeStrength },
  });

  const subtleStyle = computeNodeStyle(node, {
    isDark: true,
    activeOverlay: null,
    activeMetricResult: null,
    metricInstances: [createInstance("subtle")],
    scaleMode: "stack",
    isDiffActive: false,
    diffData: null,
    graphSettings: baseSettings,
    getPartition: () => null,
  });

  const normalStyle = computeNodeStyle(node, {
    isDark: true,
    activeOverlay: null,
    activeMetricResult: null,
    metricInstances: [createInstance("normal")],
    scaleMode: "stack",
    isDiffActive: false,
    diffData: null,
    graphSettings: baseSettings,
    getPartition: () => null,
  });

  const strongStyle = computeNodeStyle(node, {
    isDark: true,
    activeOverlay: null,
    activeMetricResult: null,
    metricInstances: [createInstance("strong")],
    scaleMode: "stack",
    isDiffActive: false,
    diffData: null,
    graphSettings: baseSettings,
    getPartition: () => null,
  });

  assert.ok(
    normalStyle.size > subtleStyle.size,
    `Normal size (${normalStyle.size}) should be strictly larger than subtle size (${subtleStyle.size})`
  );
  assert.ok(
    strongStyle.size > normalStyle.size,
    `Strong size (${strongStyle.size}) should be strictly larger than normal size (${normalStyle.size})`
  );
});

test("compact multi-select state transitions maintain domain empty-array-equals-all convention", () => {
  const allCategories = ["CLAIM", "CONCLUSION", "HYPOTHESIS", "Entity"];

  // Toggle when currently all (empty array)
  function toggle(all: string[], selected: string[], opt: string): string[] {
    const isNone = selected.length === 1 && selected[0] === "__NONE__";
    const isAll = !isNone && (selected.length === 0 || selected.length === all.length);

    if (isNone) return [opt];
    if (isAll) return all.filter((o) => o !== opt);
    if (selected.includes(opt)) {
      const next = selected.filter((o) => o !== opt);
      return next.length === 0 ? ["__NONE__"] : next;
    }
    const next = [...selected, opt];
    return next.length === all.length ? [] : next;
  }

  // 1. Initial state [] (all) -> deselect "Entity"
  const afterDeselect = toggle(allCategories, [], "Entity");
  assert.deepEqual(afterDeselect, ["CLAIM", "CONCLUSION", "HYPOTHESIS"]);

  // 2. Select "Entity" back -> should normalize back to [] (all)
  const afterReSelect = toggle(allCategories, afterDeselect, "Entity");
  assert.deepEqual(afterReSelect, []);

  // 3. Clear all -> sentinel "__NONE__"
  const cleared = ["__NONE__"];
  // 4. Select "CLAIM" while cleared -> ["CLAIM"]
  const pickedOne = toggle(allCategories, cleared, "CLAIM");
  assert.deepEqual(pickedOne, ["CLAIM"]);
});

test("scientific parameter values parse small floats without exponential truncation", () => {
  const parseNum = (raw: string, type: string) => {
    if (type === "integer") return parseInt(raw, 10);
    return parseFloat(raw);
  };

  assert.equal(parseNum("0.0001", "number"), 0.0001);
  assert.equal(parseNum("1e-4", "number"), 0.0001);
  assert.equal(parseNum("0.85", "number"), 0.85);
  assert.equal(parseNum("20", "integer"), 20);
});


