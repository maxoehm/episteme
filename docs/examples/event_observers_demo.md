# Demo — Composing Observers

The script examples/event_observers_demo.py shows how to combine observers for logs, metrics, and JSONL.

Running:

- Ensure the output folder exists or use a JsonlRunObserver that creates parents automatically.
- Execute: python examples/event_observers_demo.py
- Expected output: info logs and a printed overall acceptance rate; JSONL lines at runs/demo/events.jsonl.

Code sketch:

- Create a SimpleEventEmitter
- Create LoggingObserver, MetricsObserver, and JsonlRunObserver
- Wrap the JSONL observer in a context manager
- Register a CompositeObserver ([...])
- Emit example events (dense candidates, reranker score, triple committed)

Tips:

- Add LangfuseObserver to the composite when Langfuse is configured to see spans.
