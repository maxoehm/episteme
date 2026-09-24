import os
from episteme_pipeline import Pipeline, Phase3Config, Phase2Config
from episteme_pipeline.config import ExecutionConfig, PipelineConfig, Phase3bConfig, Phase5Config
from episteme_pipeline.graph import Neo4jGraphReader, Neo4jGraphWriter, Neo4jProcessingGraph
from llama_index.embeddings.litellm import LiteLLMEmbedding
from llama_index.llms.litellm import LiteLLM
from episteme_pipeline.phases.phase3_global_relations.rerankers import SentenceTransformerCrossEncoderReranker
from episteme_pipeline.phases.phase1_foundation import Phase1Runner
from episteme_pipeline.phases.phase2_entity_discovery import Phase2Runner
from episteme_pipeline.phases.phase3_global_relations import Phase3Runner
from episteme_pipeline.phases.phase3b_consolidation import Phase3bLatentConsolidationRunner
from episteme_pipeline.phases.phase4_argument_mining import Phase4Runner
from episteme_pipeline.phases.phase4_entity_maturation import Phase4EntityMaturationRunner
from episteme_pipeline.phases.phase3_global_relations.dense_retrieval_extractor import DenseRetrievalGlobalRelationExtractor
from episteme_pipeline.phases.phase3_global_relations.rerankers import CrossEncoderRelationReranker
from episteme_pipeline.events import EventEmitter, NoOpEventEmitter

from dotenv import load_dotenv

from episteme_pipeline.protocols.extractors import ensure_embedding_model

def _init_components(event_emitter: EventEmitter = None):
    """Initialize shared components for evaluation pipelines.

    Parameters
    ----------
    event_emitter : EventEmitter, optional
        Event bus to publish telemetry and pipeline events.

    Returns
    -------
    tuple
        Tuple containing (llm, embed_model, reranker, graph_reader,
        projection_graph, checkpoint_store, cfg).
    """
    load_dotenv()
    api_key = os.getenv("LITELLM_API_KEY") or os.getenv("OPENAI_API_KEY", "")
    api_base = os.getenv("LITELLM_API_BASE")
    llm_kwargs = {
        "model": os.getenv("LLM_MODEL", "openai/gpt-4o-mini"),
        "api_key": api_key,
    }
    if api_base:
        llm_kwargs["api_base"] = api_base
    llm = LiteLLM(**llm_kwargs)
    
    default_embed = "openai/text-embedding-3-small" if api_key else "sentence-transformers/all-MiniLM-L6-v2"
    embed_model_name = os.getenv("EMBED_MODEL", default_embed)
    if embed_model_name.startswith("local:") or "MiniLM" in embed_model_name or "huggingface" in embed_model_name or not api_key:
        from sentence_transformers import SentenceTransformer
        clean_name = embed_model_name.replace("local:", "").replace("huggingface/", "")
        if clean_name == "openai/text-embedding-3-small" or not clean_name:
            clean_name = "sentence-transformers/all-MiniLM-L6-v2"
        embed_model = ensure_embedding_model(SentenceTransformer(clean_name))
    else:
        embed_kwargs = {"model_name": embed_model_name, "api_key": api_key}
        if api_base:
            embed_kwargs["api_base"] = api_base
        embed_model = ensure_embedding_model(LiteLLMEmbedding(**embed_kwargs))
    reranker = SentenceTransformerCrossEncoderReranker(model_name=os.getenv("RERANKER_MODEL", "Qwen/Qwen3-Reranker-0.6B"))
    
    neo4j_url = os.getenv("NEO4J_URL", "neo4j://127.0.0.1:7687")
    neo4j_user = os.getenv("NEO4J_USERNAME", "neo4j")
    neo4j_password = os.getenv("NEO4J_PASSWORD", "neo4jdbpass")
    neo4j_db = os.getenv("NEO4J_DATABASE", "neo4j")

    graph_reader = Neo4jGraphReader(url=neo4j_url, username=neo4j_user, password=neo4j_password, database=neo4j_db)
    projection_graph = Neo4jGraphWriter(url=neo4j_url, username=neo4j_user, password=neo4j_password, database=neo4j_db)
    checkpoint_store = Neo4jProcessingGraph(url=neo4j_url, username=neo4j_user, password=neo4j_password, database=neo4j_db)
    
    cfg = PipelineConfig(
        execution=ExecutionConfig(project_artifacts_to_graph=True),
        phase2=Phase2Config(max_gleanings=2),
        phase3=Phase3Config(dense_similarity_threshold=0.8),
        phase3b=Phase3bConfig(dense_similarity_threshold=0.8),
    )
    
    # Wrap LLM with cache if needed, similar to pipeline_full_run.py
    from episteme_pipeline.llm.cache import DiskCachedStructuredLLM, default_cache_dir
    from episteme_pipeline.llm.structured import ensure_structured_llm
    llm = DiskCachedStructuredLLM(
        ensure_structured_llm(llm, use_cache=False, event_emitter=event_emitter),
        cache_dir=default_cache_dir(cfg.execution.runs_dir),
    )
    
    return llm, embed_model, reranker, graph_reader, projection_graph, checkpoint_store, cfg

def build_l2_eval_pipeline(event_emitter: EventEmitter = None) -> Pipeline:
    """Build a pipeline up to Phase 3 for SciERC evaluation.

    Parameters
    ----------
    event_emitter : EventEmitter, optional
        Event bus to publish telemetry and pipeline events.

    Returns
    -------
    Pipeline
        Configured L2 evaluation pipeline.
    """
    llm, embed_model, reranker, graph_reader, projection_graph, checkpoint_store, cfg = _init_components(event_emitter)
    
    cross_reranker = CrossEncoderRelationReranker(reranker)
    global_extractor = DenseRetrievalGlobalRelationExtractor(llm, embed_model, cross_reranker, cfg.phase3)
    
    phases = [
        Phase1Runner(cfg.phase1, llm=llm, embedding_model=embed_model, graph_store=projection_graph),
        Phase2Runner(cfg.phase2, cfg.graph_schema, llm=llm, embedding_model=embed_model, graph_store=checkpoint_store, cross_encoder=reranker),
        Phase3Runner(cfg.phase3, cfg.graph_schema, llm=llm, embedding_model=embed_model, graph_store=graph_reader, global_extractor=global_extractor)
    ]
    
    return Pipeline(phases=phases, config=cfg, graph_reader=graph_reader, projection_graph=projection_graph, checkpoint_store=checkpoint_store, event_emitter=event_emitter or NoOpEventEmitter())

def build_l3_eval_pipeline(event_emitter: EventEmitter = None) -> Pipeline:
    """Build a pipeline up to Phase 4 for Arg-Microtexts evaluation.

    Parameters
    ----------
    event_emitter : EventEmitter, optional
        Event bus to publish telemetry and pipeline events.

    Returns
    -------
    Pipeline
        Configured L3 evaluation pipeline.
    """
    llm, embed_model, reranker, graph_reader, projection_graph, checkpoint_store, cfg = _init_components(event_emitter)
    
    cross_reranker = CrossEncoderRelationReranker(reranker)
    global_extractor = DenseRetrievalGlobalRelationExtractor(llm, embed_model, cross_reranker, cfg.phase3)
    
    phases = [
        Phase1Runner(cfg.phase1, llm=llm, embedding_model=embed_model, graph_store=projection_graph),
        Phase2Runner(cfg.phase2, cfg.graph_schema, llm=llm, embedding_model=embed_model, graph_store=checkpoint_store, cross_encoder=reranker),
        Phase3Runner(cfg.phase3, cfg.graph_schema, llm=llm, embedding_model=embed_model, graph_store=graph_reader, global_extractor=global_extractor),
        Phase3bLatentConsolidationRunner(cfg.phase3b, embedding_model=embed_model, graph_store=graph_reader),
        Phase4EntityMaturationRunner(cfg.phase4_maturation, llm=llm, graph_store=checkpoint_store, embedding_model=embed_model),
        Phase4Runner(cfg.phase4, cfg.graph_schema, llm=llm, embedding_model=embed_model, graph_store=checkpoint_store, global_extractor=global_extractor)
    ]
    
    return Pipeline(phases=phases, config=cfg, graph_reader=graph_reader, projection_graph=projection_graph, checkpoint_store=checkpoint_store, event_emitter=event_emitter or NoOpEventEmitter())
