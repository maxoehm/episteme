/**
 * Typed HTTP client for GLP Studio REST API.
 */

import type {
  AvailableInputDoc,
  Capabilities,
  ComputeOverlayRequest,
  ConfigPatch,
  ConfigView,
  CypherResult,
  GraphDiffView,
  GraphView,
  InvalidationPreview,
  LangfuseStatusResponse,
  LangfuseTestRequest,
  Neo4jConnectPayload,
  Neo4jConnectResponse,
  Neo4jStatusResponse,
  Overlay,
  PromptResolveRequest,
  PromptResolveResponse,
  RunDetail,
  RunSummary,
  StartRunPayload,
  ExecuteMetricRequest,
  ExecutionStatusResponse,
  MetricDescriptor,
  MetricExecutionQueuedResponse,
  MetricResult,
  RunLangfuseResponse,
  EngineSettings,
  EngineSettingsPatch,
  PredicateMapping,
  SchemaConfig,
  UnmappedPredicateInfo,
} from "./types.ts";

const BASE_URL = "";

async function handleResponse<T>(res: Response): Promise<T> {
  if (!res.ok) {
    let errorData: any;
    try {
      errorData = await res.json();
    } catch {
      errorData = { title: res.statusText, status: res.status };
    }
    throw errorData;
  }
  return res.json();
}

export const api = {
  async getHealth(): Promise<{ status: string }> {
    const res = await fetch(`${BASE_URL}/api/health`);
    return handleResponse(res);
  },

  async getCapabilities(): Promise<Capabilities> {
    const res = await fetch(`${BASE_URL}/api/capabilities`);
    return handleResponse(res);
  },

  async getSchema(): Promise<Record<string, any>> {
    const res = await fetch(`${BASE_URL}/api/schema`);
    return handleResponse(res);
  },

  async listRuns(): Promise<RunSummary[]> {
    const res = await fetch(`${BASE_URL}/api/runs`);
    return handleResponse(res);
  },

  async getRun(runId: string): Promise<RunDetail> {
    const res = await fetch(`${BASE_URL}/api/runs/${encodeURIComponent(runId)}`);
    return handleResponse(res);
  },

  async startRun(payload: StartRunPayload): Promise<RunSummary> {
    const res = await fetch(`${BASE_URL}/api/runs`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    return handleResponse(res);
  },

  async cancelRun(runId: string): Promise<RunSummary> {
    const res = await fetch(`${BASE_URL}/api/runs/${encodeURIComponent(runId)}/cancel`, {
      method: "POST",
    });
    return handleResponse(res);
  },

  async getRunGraph(runId: string, budget?: number, useRunSchema = false): Promise<GraphView> {
    const params = new URLSearchParams();
    if (budget) params.set("budget", budget.toString());
    if (useRunSchema) params.set("use_run_schema", "true");
    const query = params.toString() ? `?${params.toString()}` : "";
    const res = await fetch(`${BASE_URL}/api/runs/${encodeURIComponent(runId)}/graph${query}`);
    return handleResponse(res);
  },

  async getEvidence(runId: string, nodeId: string): Promise<any> {
    const res = await fetch(
      `${BASE_URL}/api/runs/${encodeURIComponent(runId)}/evidence/${encodeURIComponent(nodeId)}`
    );
    return handleResponse(res);
  },

  async getRunLangfuseStats(
    runId: string,
    options?: { host?: string; publicKey?: string; secretKey?: string; limit?: number }
  ): Promise<RunLangfuseResponse> {
    const params = new URLSearchParams();
    if (options?.host) params.set("host", options.host);
    if (options?.publicKey) params.set("public_key", options.publicKey);
    if (options?.secretKey) params.set("secret_key", options.secretKey);
    if (options?.limit) params.set("limit", options.limit.toString());
    const query = params.toString() ? `?${params.toString()}` : "";
    const res = await fetch(`${BASE_URL}/api/runs/${encodeURIComponent(runId)}/langfuse${query}`);
    return handleResponse(res);
  },

  async executeCypher(query: string, params?: Record<string, any>, limit?: number): Promise<CypherResult> {
    const res = await fetch(`${BASE_URL}/api/graph/cypher`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query, params: params || {}, limit }),
    });
    return handleResponse(res);
  },

  async getNeo4jStatus(): Promise<Neo4jStatusResponse> {
    const res = await fetch(`${BASE_URL}/api/graph/status`);
    return handleResponse(res);
  },

  async connectNeo4j(payload: Neo4jConnectPayload): Promise<Neo4jConnectResponse> {
    const res = await fetch(`${BASE_URL}/api/graph/connect`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    return handleResponse(res);
  },

  async disconnectNeo4j(): Promise<{ status: string; neo4j: boolean }> {
    const res = await fetch(`${BASE_URL}/api/graph/disconnect`, {
      method: "POST",
    });
    return handleResponse(res);
  },

  async getNeo4jGraphView(limit?: number, layer?: number): Promise<GraphView> {
    const params = new URLSearchParams();
    if (limit) params.set("limit", limit.toString());
    if (layer) params.set("layer", layer.toString());
    const query = params.toString() ? `?${params.toString()}` : "";
    const res = await fetch(`${BASE_URL}/api/graph/view${query}`);
    return handleResponse(res);
  },

  async expandNeo4jGraph(seeds: string[], depth = 1, limit?: number): Promise<GraphView> {
    const params = new URLSearchParams();
    seeds.forEach((s) => params.append("seeds", s));
    params.set("depth", depth.toString());
    if (limit) params.set("limit", limit.toString());
    const res = await fetch(`${BASE_URL}/api/graph/expand?${params.toString()}`);
    return handleResponse(res);
  },

  async listOverlays(graphVersion?: string): Promise<Overlay[]> {
    const params = new URLSearchParams();
    if (graphVersion) params.set("graph_version", graphVersion);
    const query = params.toString() ? `?${params.toString()}` : "";
    const res = await fetch(`${BASE_URL}/api/overlays${query}`);
    return handleResponse(res);
  },

  async computeOverlay(payload: ComputeOverlayRequest): Promise<Overlay> {
    const res = await fetch(`${BASE_URL}/api/overlays`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    return handleResponse(res);
  },

  async getEffectiveConfig(profileId?: string): Promise<ConfigView> {
    const params = new URLSearchParams();
    if (profileId) params.set("profile_id", profileId);
    const query = params.toString() ? `?${params.toString()}` : "";
    const res = await fetch(`${BASE_URL}/api/config/effective${query}`);
    return handleResponse(res);
  },

  async listProfiles(): Promise<string[]> {
    const res = await fetch(`${BASE_URL}/api/config/profiles`);
    return handleResponse(res);
  },

  async previewInvalidation(payload: ConfigPatch): Promise<InvalidationPreview> {
    const res = await fetch(`${BASE_URL}/api/config/invalidation-preview`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    return handleResponse(res);
  },

  async resolvePrompts(payload: PromptResolveRequest): Promise<PromptResolveResponse> {
    const res = await fetch(`${BASE_URL}/api/config/prompts/resolve`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    return handleResponse(res);
  },

  async getAvailableInputs(): Promise<AvailableInputDoc[]> {
    const res = await fetch(`${BASE_URL}/api/config/inputs`);
    return handleResponse(res);
  },

  async uploadInputFile(file: File): Promise<AvailableInputDoc> {
    const formData = new FormData();
    formData.append("file", file);
    const res = await fetch(`${BASE_URL}/api/config/inputs/upload`, {
      method: "POST",
      body: formData,
    });
    return handleResponse(res);
  },

  async getLangfuseStatus(): Promise<LangfuseStatusResponse> {
    const res = await fetch(`${BASE_URL}/api/config/langfuse/status`);
    return handleResponse(res);
  },

  async testLangfuseConnection(payload: LangfuseTestRequest): Promise<LangfuseStatusResponse> {
    const res = await fetch(`${BASE_URL}/api/config/langfuse/test`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    return handleResponse(res);
  },

  async getMetricDefinitions(): Promise<MetricDescriptor[]> {
    const res = await fetch(`${BASE_URL}/api/metrics/definitions`);
    return handleResponse(res);
  },

  async executeMetric(
    payload: ExecuteMetricRequest,
    signal?: AbortSignal
  ): Promise<MetricResult | MetricExecutionQueuedResponse> {
    const res = await fetch(`${BASE_URL}/api/metric-executions`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
      signal,
    });
    return handleResponse(res);
  },

  async getMetricExecution(
    executionId: string,
    signal?: AbortSignal
  ): Promise<ExecutionStatusResponse> {
    const res = await fetch(`${BASE_URL}/api/metric-executions/${encodeURIComponent(executionId)}`, {
      signal,
    });
    return handleResponse(res);
  },

  async cancelMetricExecution(
    executionId: string
  ): Promise<{ execution_id: string; status: string }> {
    const res = await fetch(`${BASE_URL}/api/metric-executions/${encodeURIComponent(executionId)}`, {
      method: "DELETE",
    });
    return handleResponse(res);
  },

  async getRunDiff(
    baseId: string,
    targetId: string,
    weightShiftThreshold: number = 0.15
  ): Promise<GraphDiffView> {
    const params = new URLSearchParams({
      base_id: baseId,
      target_id: targetId,
      weight_shift_threshold: weightShiftThreshold.toString(),
    });
    const res = await fetch(`${BASE_URL}/api/diff/runs?${params.toString()}`);
    return handleResponse(res);
  },

  async getEngineSettings(): Promise<EngineSettings> {
    const res = await fetch(`${BASE_URL}/api/engine/settings`);
    return handleResponse(res);
  },

  async updateEngineSettings(patch: EngineSettingsPatch): Promise<EngineSettings> {
    const res = await fetch(`${BASE_URL}/api/engine/settings`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(patch),
    });
    return handleResponse(res);
  },

  async resetEngineSettings(): Promise<EngineSettings> {
    const res = await fetch(`${BASE_URL}/api/engine/settings/reset`, {
      method: "POST",
    });
    return handleResponse(res);
  },

  async getEngineSchema(): Promise<SchemaConfig> {
    const res = await fetch(`${BASE_URL}/api/engine/schema`);
    return handleResponse(res);
  },

  async getUnmappedPredicates(): Promise<UnmappedPredicateInfo[]> {
    const res = await fetch(`${BASE_URL}/api/engine/unmapped-predicates`);
    return handleResponse(res);
  },

  async mapUnmappedPredicate(mapping: PredicateMapping): Promise<EngineSettings> {
    const res = await fetch(`${BASE_URL}/api/engine/map-predicate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(mapping),
    });
    return handleResponse(res);
  },
};

