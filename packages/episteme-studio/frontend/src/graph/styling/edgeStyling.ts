import type { StudioEdge } from "../../api/types.ts";
import type { EdgeStyleContext } from "./types.ts";

export interface ComputedEdgeStyle {
  stroke: string;
  lineDash?: [number, number];
  lineWidth: number;
  endArrow: boolean;
  labelText: string;
  labelFill: string;
  labelFontSize: number;
  labelBackground: boolean;
  labelBackgroundFill: string;
  labelBackgroundRadius: number;
  cursor: string;
  halo: boolean;
  haloStroke: string;
  haloLineWidth: number;
}

/**
 * Pure function computing G6 edge styling attributes from domain edge & context.
 * Transparently integrates dynamic schema polarity and open-vocabulary alias resolution.
 */
export function computeEdgeStyle(edge: StudioEdge, ctx: EdgeStyleContext): ComputedEdgeStyle {
  const { isDark, graphSettings, activeOverlay, activeMetricResult, isDiffActive, diffData, getPolarity } = ctx;

  // 1. Dynamic polarity resolution: Schema/alias mapping takes priority, falls back to edge payload
  const polarity = getPolarity(edge.type) ?? edge.polarity ?? (edge.props as any)?.polarity ?? null;

  let stroke = isDark ? "#94a3b8" : "#64748b"; // neutral (0)
  let lineDash: [number, number] | undefined = undefined;

  if (polarity === 1) {
    stroke = "#10b981"; // support (+1) emerald
  } else if (polarity === -1) {
    stroke = "#ef4444"; // attack (-1) red
  } else if (polarity === 0) {
    stroke = isDark ? "#94a3b8" : "#64748b"; // neutral (0) solid
  } else {
    // null or undefined: open-vocabulary unmapped predicate (D-15)
    stroke = isDark ? "#64748b" : "#94a3b8";
    lineDash = [4, 4];
  }

  // 2. Diff mode edge styling
  if (isDiffActive && diffData) {
    const edgeStatus = diffData.edge_diff[edge.id];
    if (edgeStatus === "polarity_inverted") {
      stroke = "#f59e0b"; // amber
      lineDash = [6, 3];
    } else if (edgeStatus === "gained") {
      stroke = "#10b981"; // emerald
    } else if (edgeStatus === "lost") {
      stroke = "#ef4444"; // red
      lineDash = [4, 4];
    }
  }

  let lineWidth =
    edge.weight !== null && edge.weight !== undefined
      ? Math.max(1, Math.min(3.5, Math.round(edge.weight * 3)))
      : 1.5;

  if (isDiffActive && diffData) {
    const edgeStatus = diffData.edge_diff[edge.id];
    if (edgeStatus === "polarity_inverted") {
      lineWidth = 3.5;
    } else if (edgeStatus === "gained") {
      lineWidth = 2.5;
    }
  }

  // Apply customizable edge thickness multiplier
  lineWidth = Math.max(0.5, Math.round(lineWidth * graphSettings.edgeThicknessMultiplier * 2) / 2);

  // 3. Metric Overlay edge styling (Check across all active instances)
  const activeInstances = (ctx.metricInstances || []).filter(
    (inst) => inst.status === "completed" && inst.result && inst.styling?.enabled !== false
  );

  let affectedEdgeDetail = null;
  for (const inst of activeInstances) {
    const aff = inst.result?.affected_edges.find(
      (ae) =>
        ae.relationship_id === edge.id ||
        (ae.source_node_id === edge.source && ae.target_node_id === edge.target)
    );
    if (aff) {
      affectedEdgeDetail = aff;
      break;
    }
  }

  if (!affectedEdgeDetail && activeMetricResult) {
    affectedEdgeDetail = activeMetricResult.affected_edges.find(
      (ae) =>
        ae.relationship_id === edge.id ||
        (ae.source_node_id === edge.source && ae.target_node_id === edge.target)
    );
  }

  if (affectedEdgeDetail) {
    if (affectedEdgeDetail.role === "support") {
      stroke = "#10b981";
      lineDash = undefined;
      lineWidth = Math.max(2, Math.min(5, Math.round(Math.abs(affectedEdgeDetail.contribution || affectedEdgeDetail.weight || 1) * 3)));
    } else if (affectedEdgeDetail.role === "attack") {
      stroke = "#ef4444";
      lineDash = [6, 4];
      lineWidth = Math.max(2, Math.min(5, Math.round(Math.abs(affectedEdgeDetail.contribution || affectedEdgeDetail.weight || 1) * 3)));
    } else if (affectedEdgeDetail.role === "undercut") {
      stroke = "#f59e0b";
      lineDash = [4, 4];
      lineWidth = 2.5;
    }
  }

  // 4. Active Overlay edge styling (e.g. Tenability TS_edge)
  if (activeOverlay?.edge_values) {
    const val = activeOverlay.edge_values[edge.id];
    if (val !== undefined && val !== null) {
      if (activeOverlay.kind === "tenability") {
        const ts = typeof val === "number" ? val : 0;
        if (ts >= 0.8) {
          stroke = "#10b981"; // emerald
          lineWidth = Math.max(2, lineWidth);
        } else if (ts >= 0.5) {
          stroke = "#f59e0b"; // amber
          lineWidth = Math.max(2, lineWidth);
        } else {
          stroke = "#f43f5e"; // rose/red
          lineDash = [4, 4];
          lineWidth = Math.max(2.5, lineWidth);
        }
      }
    }
  }

  return {
    stroke,
    lineDash,
    lineWidth,
    endArrow: true,
    labelText: graphSettings.showEdgeLabels ? edge.type : "",
    labelFill: isDark ? "#8b949e" : "#57606a",
    labelFontSize: 9,
    labelBackground: true,
    labelBackgroundFill: isDark ? "#161b22" : "#ffffff",
    labelBackgroundRadius: 2,
    cursor: "pointer",
    halo: false,
    haloStroke: "transparent",
    haloLineWidth: 0,
  };
}
