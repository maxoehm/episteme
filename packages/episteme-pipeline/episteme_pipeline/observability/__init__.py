"""
Observability hooks for tracing LLM calls and phase transitions.

Default integration: Langfuse (@observe decorator pattern).
Swap by replacing the trace() context manager with any OpenTelemetry-compatible
backend (Arize, Weights & Biases, MLflow, etc.).
"""

from .logging import (
    DEFAULT_NOISY_LOGGERS,
    configure_pipeline_logging,
    run_folder_logger,
    silence_noisy_loggers,
)

__all__ = [
    "DEFAULT_NOISY_LOGGERS",
    "configure_pipeline_logging",
    "run_folder_logger",
    "silence_noisy_loggers",
]
