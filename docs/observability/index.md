# Observability Overview

The pipeline uses an event‑driven observability architecture. Components publish small, typed "domain events"; observers
translate those events into outputs like logs, metrics, JSONL research traces, and Langfuse spans. This decouples
business logic from telemetry, makes experiments reproducible, and lets you turn sinks on/off per run.

Key ideas:

- Domain events, not framework‑specific traces
- Multiple observers can subscribe to the same event stream
- Optional Langfuse integration, enabled only when configured
- JSONL logs double as research artifacts for audit and replay

See also:

- [events.md](events.md) for the complete event reference catalog, observer setups, and how-to guides
- [langfuse.md](langfuse.md) to enable and interpret Langfuse spans
- [adapters-migration.md](adapters-migration.md) for moving from legacy TraceSink
- [Event System Architecture](../architecture/event-system.md) for the conceptual design, contextvar dispatch, and lifecycle

## Implementation Details

For implementation details about observability components, please refer to:

- The `pipeline/events/` module for core event definitions and emitters (`models.py`, `bus.py`, `context.py`)
- Individual observer implementations in `pipeline/events/observers.py`, `pipeline/events/progress_observer.py`, and `pipeline/events/langfuse_observer.py`
