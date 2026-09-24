# Event & Observer API

## EventEmitter Protocol

::: episteme_pipeline.events.bus.EventEmitter
    options:
      show_root_heading: false
      show_root_toc_entry: false

## EventObserver Protocol

::: episteme_pipeline.events.bus.EventObserver
    options:
      show_root_heading: false
      show_root_toc_entry: false

## Event Models

All pipeline event payload models in `pipeline/events/models.py`:

::: episteme_pipeline.events.models
    options:
      show_root_heading: false
      show_root_toc_entry: false

## Built-ins

- SimpleEventEmitter — in‑process broadcast list
- JsonlRunObserver — context‑managed JSONL writer
- LoggingObserver — level‑aware summaries
- MetricsObserver — acceptance rates and totals
- RichProgressObserver — terminal live progress bars and logger coordination (requires an interactive TTY)
- CompositeObserver — fan‑out dispatcher
- LangfuseObserver — event→span mapping (requires Langfuse)

## Concurrency & performance

- Observers should be fast; heavy work should buffer/async off the hot path.
- Consider protecting CompositeObserver with failure isolation.
