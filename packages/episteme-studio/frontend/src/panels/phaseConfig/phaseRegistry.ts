/**
 * Declarative registry of pipeline phases and parameter metadata.
 * Conforms to Open/Closed Principle (OCP): New phases can be registered here
 * without modifying UI renderers or modal shells.
 */

export interface ParameterFieldMeta {
  label: string;
  description?: string;
  unit?: string;
  defaultValue?: string | number | boolean;
  isAdvanced?: boolean;
  group?: "thresholds" | "limits" | "general";
}

export interface PhaseMetadata {
  key: string;
  canonicalOrdinal: number;
  displayName: string;
  shortLabel: string;
  category: string;
  description: string;
  isPostProcessor?: boolean;
  isMandatory?: boolean;
  configPrefix?: string;
  parameterMeta: Record<string, ParameterFieldMeta>;
  promptKeys: string[];
  executionKey?: string;
}

export const PIPELINE_DEFAULTS_KEY = "phase0";

export const CORE_DAG_PHASE_KEYS = [
  "phase1",
  "phase2",
  "schema",
  "phase3",
  "phase3b",
  "phase4_maturation",
  "phase4",
  "phase5",
  "phase6",
];

export const POST_PROCESSOR_KEYS = [
  "phase7",
];

export const PHASE_REGISTRY: Record<string, PhaseMetadata> = {
  phase0: {
    key: "phase0",
    canonicalOrdinal: 0,
    displayName: "Pipeline Defaults & Global Architecture",
    shortLabel: "Pipeline Defaults",
    category: "Baseline Setup",
    isMandatory: true,
    description:
      "Global inference baseline, dense vector representations, cross-encoder rerankers, and pipeline caching policies inherited by all computational stages.",
    parameterMeta: {
      "models.llm_model": {
        label: "Generative model",
        description: "Primary LLM for extraction, classification, and epistemic synthesis",
        defaultValue: "openai/gpt-4o-mini",
        group: "general",
      },
      "models.thinking_level": {
        label: "Model Thinking Level",
        description: "Reasoning budget / thinking depth for LLM inference (off, low, medium, high, or custom)",
        defaultValue: "off",
        group: "general",
      },
      "models.embedding_model": {
        label: "Dense embedding model",
        description: "Vector representation model for semantic search and candidate retrieval",
        defaultValue: "sentence-transformers/all-MiniLM-L6-v2",
        group: "general",
      },
      "models.reranker_model": {
        label: "Cross-encoder reranker",
        description: "Cross-encoder scoring cutoff prior to LLM relation verification",
        defaultValue: "Alibaba-NLP/gte-reranker-modernbert-base",
        group: "general",
      },
      "models.temperature": {
        label: "Sampling temperature",
        description: "Decoding temperature (0.0 for deterministic greedy sampling)",
        defaultValue: 0.0,
        group: "thresholds",
      },
      "models.seed": {
        label: "Random seed",
        description: "Reproducible random seed for stochastic sampling and clustering",
        defaultValue: 42,
        isAdvanced: true,
        group: "general",
      },
      "models.llm_api_base": {
        label: "LLM API base URL",
        description: "OpenAI-compatible server endpoint base URL",
        defaultValue: "https://api.openai.com/v1",
        isAdvanced: true,
        group: "general",
      },
      "execution.allow_phase_reuse": {
        label: "Allow phase reuse",
        description: "Permit fingerprint-based phase cache reuse across pipeline executions",
        defaultValue: true,
        group: "limits",
      },
      "execution.allow_artifact_hydration": {
        label: "Allow artifact hydration",
        description: "Hydrate artifacts directly from prior runs to skip recomputation",
        defaultValue: true,
        isAdvanced: true,
        group: "limits",
      },
      "execution.persist_run_manifests": {
        label: "Persist run manifests",
        description: "Write immutable JSON run manifests to disk",
        defaultValue: true,
        isAdvanced: true,
        group: "limits",
      },
      "execution.project_artifacts_to_graph": {
        label: "Project artifacts to graph",
        description: "Sync phase outputs into active Neo4j property graph",
        defaultValue: true,
        isAdvanced: true,
        group: "limits",
      },
      "execution.runs_dir": {
        label: "Runs directory",
        description: "Disk storage root for run execution metadata",
        defaultValue: "runs",
        isAdvanced: true,
        group: "limits",
      },
      "execution.artifacts_dir": {
        label: "Artifacts directory",
        description: "Disk storage root for persisted artifact collections",
        defaultValue: "artifacts",
        isAdvanced: true,
        group: "limits",
      },
    },
    promptKeys: [],
  },
  schema: {
    key: "schema",
    canonicalOrdinal: 0,
    displayName: "Epistemic Schema & Ontology",
    shortLabel: "Schema",
    category: "L2/L3 Ontology",
    isMandatory: true,
    description:
      "Configure decoupled node types (L2 entities), relation types, L3 argument component types, and argument relation polarities that govern prompt generation.",
    parameterMeta: {
      "graph_schema.node_types": {
        label: "L2 Entity Node Types",
        description: "Permitted entity classifications for named entity recognition and knowledge graph projection",
        defaultValue: "Concept, Person, Work, Theory, Institution",
        group: "general",
      },
      "graph_schema.relation_types": {
        label: "L2 Domain Relation Types",
        description: "Permitted relationship predicates between L2 entity mentions",
        defaultValue: "RELATED_TO, INSTANCE_OF, PART_OF, SUBCLASS_OF, SUPPORTS, REFUTES, IMPLIES, CONTRADICTS",
        group: "general",
      },
      "graph_schema.component_types": {
        label: "L3 Argument Component Types",
        description: "Epistemic argument unit types (e.g. ObservationUnit, EmpiricalStatement, TheoreticalHypothesis)",
        defaultValue: "ObservationUnit, EmpiricalStatement, TheoreticalHypothesis, CoreExpansion",
        group: "general",
      },
      "graph_schema.argument_relation_types": {
        label: "L3 Argument Relation Types",
        description: "Dialectical and inferential argument edges (e.g. ATTACKS, SUPPORTS_ARG, UNDERCUTS, SPECIALIZES)",
        defaultValue: "ATTACKS, SUPPORTS_ARG, UNDERCUTS, SPECIALIZES, CONSTRAINS, REDUCES_TO, ENTAILS, DEDUCES, COHERES_WITH, INHIBITS",
        group: "general",
      },
    },
    promptKeys: [],
  },
  phase1: {
    key: "phase1",
    canonicalOrdinal: 1,
    displayName: "Phase 1: Data Foundation",
    shortLabel: "Phase 1",
    category: "L1 Foundation",
    isMandatory: true,
    description:
      "Ingests source texts, segments content into overlapping chunks, and creates provenance-tracked document artifacts.",
    parameterMeta: {
      chunk_size: {
        label: "Chunk Size",
        description: "Target maximum token or character count per segmented chunk",
        unit: "tokens/chars",
        defaultValue: 1024,
        group: "limits",
      },
      chunk_overlap: {
        label: "Chunk Overlap",
        description: "Token/character overlap between adjacent sequential chunks",
        unit: "tokens/chars",
        defaultValue: 128,
        group: "limits",
      },
      provenance_enabled: {
        label: "Provenance Tracking",
        description: "Record exact character offsets and source file anchors for each chunk",
        defaultValue: true,
        isAdvanced: true,
        group: "general",
      },
    },
    promptKeys: [],
    executionKey: "persist_phase1_artifacts",
  },
  phase2: {
    key: "phase2",
    canonicalOrdinal: 2,
    displayName: "Phase 2: Entity & Local Relation Discovery",
    shortLabel: "Phase 2",
    category: "L2 Knowledge Graph",
    isMandatory: true,
    description:
      "Performs structured Named Entity Recognition (NER), extracts intra-chunk triples, and links entity mentions to the knowledge graph.",
    parameterMeta: {
      top_k_linking_candidates: {
        label: "Top-K Candidates",
        description: "Maximum candidates retrieved from vector store for entity linking",
        defaultValue: 10,
        group: "limits",
      },
      linking_confidence_threshold: {
        label: "Linking Confidence Threshold",
        description: "Minimum confidence score for committing an entity linking match",
        defaultValue: 0.85,
        group: "thresholds",
      },
      ner_confidence_threshold: {
        label: "NER Confidence Threshold",
        description: "Minimum confidence required to retain an extracted entity mention",
        defaultValue: 0.0,
        group: "thresholds",
      },
      local_relation_confidence_threshold: {
        label: "Local Relation Confidence Threshold",
        description: "Minimum confidence required to retain an extracted local triple",
        defaultValue: 0.0,
        group: "thresholds",
      },
      batch_size: {
        label: "Batch Size",
        description: "Number of chunks processed per LLM batch",
        defaultValue: 10,
        group: "limits",
      },
      ner_decoding_strategy: {
        label: "NER Decoding Strategy",
        description: "Structured decoding approach (e.g. nl_to_format, direct_constrained)",
        defaultValue: "nl_to_format",
        isAdvanced: true,
        group: "general",
      },
      max_gleanings: {
        label: "Max Gleanings",
        description: "Maximum iterative gleaning passes to extract missed entities",
        defaultValue: 2,
        isAdvanced: true,
        group: "limits",
      },
    },
    promptKeys: [
      "ner_prompts",
      "entity_linking_prompt_template",
      "entity_linking_prompts",
    ],
    executionKey: "persist_phase2_artifacts",
  },
  phase3: {
    key: "phase3",
    canonicalOrdinal: 3,
    displayName: "Phase 3: Global Relation Extraction",
    shortLabel: "Phase 3",
    category: "L2 Knowledge Graph",
    isMandatory: false,
    description:
      "Discovers non-local semantic relations across document sections via dense retrieval and cross-encoder reranking.",
    parameterMeta: {
      global_relation_confidence_threshold: {
        label: "Global Relation Threshold",
        description: "Minimum confidence to materialize a cross-chunk global relation edge",
        defaultValue: 0.7,
        group: "thresholds",
      },
      max_candidates_per_entity_pair: {
        label: "Max Candidates Per Pair",
        description: "Candidate ceiling evaluated per entity pair",
        defaultValue: 200,
        group: "limits",
      },
      subgraph_depth: {
        label: "Subgraph Envelope Depth",
        description: "Hop radius for expanding surrounding subgraph context",
        unit: "hops",
        defaultValue: 2,
        group: "limits",
      },
      dense_similarity_threshold: {
        label: "Dense Similarity Threshold",
        description: "Cosine similarity cutoff for dense embedding candidate retrieval",
        defaultValue: 0.8,
        group: "thresholds",
      },
      reranker_threshold: {
        label: "Reranker Threshold",
        description: "Cross-encoder scoring cutoff prior to LLM relation verification",
        defaultValue: 0.6,
        group: "thresholds",
      },
      trace_dense_retrieval: {
        label: "Trace Dense Retrieval",
        description: "Record detailed retrieval diagnostic traces in artifacts",
        defaultValue: true,
        isAdvanced: true,
        group: "general",
      },
      global_relation_decoding_strategy: {
        label: "Relation Decoding Strategy",
        description: "Structured decoding pipeline for relation extraction",
        defaultValue: "nl_to_format",
        isAdvanced: true,
        group: "general",
      },
    },
    promptKeys: ["global_relation_prompts"],
    executionKey: "persist_phase3_artifacts",
  },
  phase3b: {
    key: "phase3b",
    canonicalOrdinal: 4,
    displayName: "Phase 3b: Latent Graph Consolidation",
    shortLabel: "Phase 3b",
    category: "L2 Knowledge Graph",
    isMandatory: false,
    description:
      "Evaluates high-similarity entity pairs to consolidate latent duplicates via topological overlap and embedding similarity.",
    parameterMeta: {
      enabled: {
        label: "Phase Enabled",
        description: "Whether latent consolidation execution is enabled",
        defaultValue: true,
        group: "general",
      },
      dense_similarity_threshold: {
        label: "Dense Similarity Threshold",
        description: "Minimum cosine similarity between entity embeddings for consolidation",
        defaultValue: 0.85,
        group: "thresholds",
      },
      relation_overlap_threshold: {
        label: "Relation Overlap Threshold",
        description: "Minimum Jaccard neighborhood similarity to commit SAME_AS edge",
        defaultValue: 0.8,
        group: "thresholds",
      },
    },
    promptKeys: [],
    executionKey: "persist_phase3b_artifacts",
  },
  phase4_maturation: {
    key: "phase4_maturation",
    canonicalOrdinal: 5,
    displayName: "Phase 4: Entity Maturation (Batch Epistemic Synthesis)",
    shortLabel: "Phase 4: Maturation",
    category: "L2 Knowledge Graph",
    isMandatory: false,
    description:
      "Synthesizes mature canonical academic descriptions for entities by aggregating representative contextual envelopes near centroids.",
    parameterMeta: {
      maturation_top_k: {
        label: "Maturation Top-K",
        description: "Number of textual envelopes closest to geometric centroid retrieved",
        defaultValue: 5,
        group: "limits",
      },
      batch_size: {
        label: "Batch Size",
        description: "Number of entities synthesized concurrently in LLM calls",
        defaultValue: 10,
        group: "limits",
      },
      entity_synthesis_decoding_strategy: {
        label: "Synthesis Decoding Strategy",
        description: "Decoding method for epistemic entity synthesis",
        defaultValue: "direct_constrained",
        isAdvanced: true,
        group: "general",
      },
    },
    promptKeys: ["entity_synthesis_prompts"],
    executionKey: "persist_phase4_maturation_artifacts",
  },
  phase4: {
    key: "phase4",
    canonicalOrdinal: 6,
    displayName: "Phase 4: Argument Mining",
    shortLabel: "Phase 4: Mining",
    category: "L3 Argument Mining",
    isMandatory: false,
    description:
      "Segments Argumentative Discourse Units (ADUs), classifies argument components (ACC), and identifies support/attack relations (ARC).",
    parameterMeta: {
      acc_confidence_threshold: {
        label: "ACC Confidence Threshold",
        description: "Argument Component Classification acceptance threshold",
        defaultValue: 0.0,
        group: "thresholds",
      },
      arc_confidence_threshold: {
        label: "ARC Confidence Threshold",
        description: "Argument Relation Classification acceptance threshold",
        defaultValue: 0.65,
        group: "thresholds",
      },
      batch_size: {
        label: "Batch Size",
        description: "Number of ADUs or pairs evaluated per batch",
        defaultValue: 10,
        group: "limits",
      },
      arc_subgraph_depth: {
        label: "ARC Subgraph Depth",
        description: "Graph envelope depth supplied as context for argument relation reasoning",
        unit: "hops",
        defaultValue: 2,
        group: "limits",
      },
      arc_max_candidates_per_component: {
        label: "Max Candidates Per Component",
        description: "Maximum pairing candidates evaluated for each argument component",
        defaultValue: 10,
        group: "limits",
      },
      arc_use_priority_rank: {
        label: "ARC Priority Ranking",
        description: "Prioritize evaluation of high-plausibility argument pairs",
        defaultValue: false,
        isAdvanced: true,
        group: "limits",
      },
      acc_decoding_strategy: {
        label: "ACC Decoding Strategy",
        description: "Structured decoding strategy for component classification",
        defaultValue: "nl_to_format",
        isAdvanced: true,
        group: "general",
      },
      arc_decoding_strategy: {
        label: "ARC Decoding Strategy",
        description: "Structured decoding strategy for relation classification",
        defaultValue: "nl_to_format",
        isAdvanced: true,
        group: "general",
      },
      adu_markup_open: {
        label: "ADU Markup Open Tag",
        description: "Markup opening tag delimiter for discourse units",
        defaultValue: "<AC",
        isAdvanced: true,
        group: "general",
      },
      adu_markup_close: {
        label: "ADU Markup Close Tag",
        description: "Markup closing tag delimiter for discourse units",
        defaultValue: ">",
        isAdvanced: true,
        group: "general",
      },
    },
    promptKeys: [
      "adu_segmentation_prompt_template",
      "adu_segmentation_prompts",
      "acc_prompts",
      "arc_prompts",
    ],
    executionKey: "persist_phase4_artifacts",
  },
  phase5: {
    key: "phase5",
    canonicalOrdinal: 7,
    displayName: "Phase 5: Inter-Document Argument Web",
    shortLabel: "Phase 5",
    category: "L4 TheoryNet & Fusion",
    isMandatory: false,
    description:
      "Constructs macro argument webs, cluster graphs, and cross-document theory fusion decisions.",
    parameterMeta: {
      argument_clustering_enabled: {
        label: "Argument Clustering Enabled",
        description: "Cluster argument components into overarching topical clusters",
        defaultValue: true,
        group: "general",
      },
      theory_fusion_enabled: {
        label: "Theory Fusion Enabled",
        description: "Execute theory fusion and cross-document alignment",
        defaultValue: true,
        group: "general",
      },
      fusion_similarity_threshold: {
        label: "Fusion Similarity Threshold",
        description: "Minimum semantic similarity required to fuse theoretical constructs",
        defaultValue: 0.85,
        group: "thresholds",
      },
      cluster_layer: {
        label: "Cluster Layer",
        description: "Target graph layer for clustering (theory_atoms, l2_entities, or both)",
        defaultValue: "both",
        isAdvanced: true,
        group: "limits",
      },
    },
    promptKeys: [],
    executionKey: "persist_phase5_artifacts",
  },
  phase6: {
    key: "phase6",
    canonicalOrdinal: 8,
    displayName: "Phase 6: Epistemic Consolidation",
    shortLabel: "Phase 6",
    category: "L4 TheoryNet & Fusion",
    isMandatory: false,
    description:
      "Final graph consolidation, epistemic integrity checks, and dialectical consistency projection.",
    parameterMeta: {
      enabled: {
        label: "Phase Enabled",
        description: "Whether epistemic consolidation is active",
        defaultValue: true,
        group: "general",
      },
    },
    promptKeys: [],
    executionKey: "persist_phase6_artifacts",
  },
  execution: {
    key: "execution",
    canonicalOrdinal: 9,
    displayName: "Pipeline Execution & Persistence",
    shortLabel: "Execution",
    category: "Pipeline Runtime",
    description:
      "Controls artifact caching, manifest persistence, run hydration, and projection policies.",
    parameterMeta: {
      persist_run_manifests: {
        label: "Persist Run Manifests",
        description: "Write immutable JSON run manifests to disk",
        defaultValue: true,
        isAdvanced: true,
        group: "limits",
      },
      allow_phase_reuse: {
        label: "Allow Phase Reuse",
        description: "Permit fingerprint-based phase reuse across pipeline executions",
        defaultValue: true,
        group: "limits",
      },
      allow_artifact_hydration: {
        label: "Allow Artifact Hydration",
        description: "Hydrate artifacts directly from prior runs to skip recomputation",
        defaultValue: true,
        isAdvanced: true,
        group: "limits",
      },
      project_artifacts_to_graph: {
        label: "Project Artifacts to Graph",
        description: "Sync phase outputs into active Neo4j property graph",
        defaultValue: true,
        isAdvanced: true,
        group: "limits",
      },
      runs_dir: {
        label: "Runs Directory",
        description: "Disk storage root for run execution metadata",
        defaultValue: "runs",
        isAdvanced: true,
        group: "limits",
      },
      artifacts_dir: {
        label: "Artifacts Directory",
        description: "Disk storage root for persisted artifact collections",
        defaultValue: "artifacts",
        isAdvanced: true,
        group: "limits",
      },
    },
    promptKeys: [],
  },
  models: {
    key: "models",
    canonicalOrdinal: 0,
    displayName: "Methodological Model Stack (D-14)",
    shortLabel: "Models",
    category: "Inference & Embedding",
    description:
      "Select generative LLMs, dense embedding representations, cross-encoder rerankers, temperature, and reproducible random seeds.",
    parameterMeta: {
      llm_model: {
        label: "Generative LLM Model",
        description: "Model identifier for extraction, classification, and epistemic synthesis",
        defaultValue: "openai/gpt-4o-mini",
        group: "general",
      },
      thinking_level: {
        label: "Thinking Level",
        description: "Reasoning budget / thinking depth for LLM inference (off, low, medium, high, or custom)",
        defaultValue: "off",
        group: "general",
      },
      embedding_model: {
        label: "Dense Embedding Model",
        description: "Dense vector model for semantic similarity and candidate retrieval",
        defaultValue: "sentence-transformers/all-MiniLM-L6-v2",
        group: "general",
      },
      reranker_model: {
        label: "Cross-Encoder Reranker",
        description: "Cross-encoder scoring cutoff prior to LLM relation verification",
        defaultValue: "Alibaba-NLP/gte-reranker-modernbert-base",
        group: "general",
      },
      temperature: {
        label: "Sampling Temperature",
        description: "Decoding temperature (0.0 for deterministic greedy sampling)",
        defaultValue: 0.0,
        group: "thresholds",
      },
      seed: {
        label: "Random Seed",
        description: "Reproducible random seed for stochastic sampling / clustering",
        defaultValue: 42,
        isAdvanced: true,
        group: "general",
      },
      llm_api_base: {
        label: "LLM API Endpoint Base URL",
        description: "OpenAI-compatible / LiteLLM server endpoint (optional)",
        defaultValue: "https://api.openai.com/v1",
        isAdvanced: true,
        group: "general",
      },
    },
    promptKeys: [],
  },
  phase7: {
    key: "phase7",
    canonicalOrdinal: 10,
    displayName: "Theoretical Enrichment & Tenability Evaluation",
    shortLabel: "Tenability Solver",
    category: "Analysis & Post-Processing",
    isPostProcessor: true,
    isMandatory: false,
    configPrefix: "theoretical_enrichment",
    description:
      "Formalizes structuralist metatheory (Stegmüller 1976; Balzer et al. 1987). Projects empirical observation clusters into theory-specific parametric spaces and calculates local and edge tenability under blur bounds.",
    parameterMeta: {
      enabled: {
        label: "Enable Post-Processor",
        description: "Whether post-processing theoretical enrichment & tenability evaluation is enabled",
        defaultValue: true,
        group: "general",
      },
      tenability_threshold: {
        label: "Anomaly Threshold",
        description: "Tenability score cutoff below which an epistemic anomaly is flagged",
        defaultValue: 0.5,
        group: "thresholds",
      },
      weight_local: {
        label: "Local Law Weight",
        description: "Relative weight of local core law satisfaction in aggregated score",
        defaultValue: 0.5,
        group: "thresholds",
      },
      weight_edge: {
        label: "Edge Constraint Weight",
        description: "Relative weight of intertheoretical constraint consistency in aggregated score",
        defaultValue: 0.5,
        group: "thresholds",
      },
    },
    promptKeys: [],
    executionKey: "persist_phase7_artifacts",
  },
};

/**
 * Register a dynamic or custom phase / post-processor into the global runtime registry.
 */
export function registerCustomPhase(meta: PhaseMetadata): void {
  PHASE_REGISTRY[meta.key] = meta;
}

/**
 * Check if a phase is considered mandatory for pipeline execution.
 */
export function isPhaseMandatory(phaseKey: string): boolean {
  return Boolean(PHASE_REGISTRY[phaseKey]?.isMandatory);
}

/**
 * Check if a phase is classified as an analytical post-processor.
 */
export function isPhasePostProcessor(phaseKey: string): boolean {
  return Boolean(PHASE_REGISTRY[phaseKey]?.isPostProcessor);
}

/**
 * Get all registered phases sorted in canonical pipeline execution order.
 */
export function getAllRegisteredPhases(): PhaseMetadata[] {
  return Object.values(PHASE_REGISTRY).sort(
    (a, b) => a.canonicalOrdinal - b.canonicalOrdinal
  );
}


