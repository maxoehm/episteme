# Migrating From TraceSink

The legacy TraceSink API is still used in parts of the codebase. New code should emit domain events. For incremental
migration:

- Wrap legacy tracing with TraceSinkToEventEmitterAdapter and progressively map TraceSink spans to domain events.
- Prefer emitting domain events directly in new code paths.
- Keep Langfuse runs grouped via run_observability_context.

Status:

- The adapter scaffold exists; event forwarding/mapping should be implemented so ComponentStarted/Completed actually
  reach observers.
- Once events cover the required signals, retire direct TraceSink usage.
