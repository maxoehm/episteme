# Run Persistence Tests

This directory contains tests that verify the correct behavior of run manifest persistence in various edge cases.

## Key Scenarios Tested

1. **Normal Operation**: Regular pipeline execution with standard artifact generation
2. **Empty Results**: Pipeline completion when no entities are found/processed  
3. **Directory Creation**: Automatic creation of `.pipeline_runs` directory when missing
4. **Nested Paths**: Handling of deeply nested run directory paths
5. **Error Handling**: Graceful handling of persistence errors

## Reproducing Previous Issues

The tests in this directory specifically address a previous `FileNotFoundError` that occurred when trying to write run manifests. The error message was:

```
FileNotFoundError: [Errno 2] No such file or directory: '.pipeline_runs/run-{uuid}.json'
```

This happened when the pipeline completed successfully but with no entities processed (resulting in 0 candidates and 0 triples).

## Test Results

All tests should pass, demonstrating that:

- Manifest persistence works correctly even with empty results
- Directory creation is handled automatically
- Edge cases are properly handled
- The previous FileNotFoundError scenario is resolved

## Running Tests

```bash
uv run pytest tests/unit/runs/ -v
```

