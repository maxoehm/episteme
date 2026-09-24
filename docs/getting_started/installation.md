# Installation Guide

This guide walks you through setting up the Episteme monorepo workspace, installing required system tools, and verifying the installation.

---

## Monorepo Setup with `uv`

Episteme is structured as a `uv` workspace comprising three interconnected packages:
* `episteme-pipeline`: The core theory graph extraction engine.
* `epistemetrics`: Standalone scientific evaluation and coherence metric library.
* `episteme-studio`: Run-oriented visual workbench and API service.

Clone the repository and sync all workspace members and development dependencies:

```bash
# Clone the repository
git clone https://github.com/maoem/network-construct.git
cd network-construct

# Synchronize virtual environment and all workspace packages
uv sync
```

This command automatically resolves the unified lockfile, sets up an isolated Python virtual environment, and installs all local workspace packages in editable mode.

---

## System Dependencies

### Pandoc Installation
Pandoc is required for academic document normalization:

- "macOS (Homebrew)"
    ```bash
    brew install pandoc
    ```

- "Ubuntu / Debian"
    ```bash
    sudo apt-get update && sudo apt-get install -y pandoc
    ```

Verify installation:
```bash
pandoc --version
```

---

## Verifying Installation

Verify that the core engine and studio CLI entrypoints are functional:

### Verify Pipeline Engine
```bash
uv run python -c "import pipeline; print('Pipeline engine installed successfully')"
```
Expected output:
```text
Pipeline engine installed successfully
```

### Verify Episteme Studio CLI
```bash
uv run episteme-studio --help
```
Expected output:
```text
usage: episteme-studio [-h] {serve} ...

Episteme Studio — workbench for Episteme runs and artifacts.

positional arguments:
  {serve}
    serve     Start the Episteme Studio web server.
```

---

## Next Steps

Now that your workspace is ready, configure your database credentials and OpenAPI model endpoints in the [Configuration Guide](configuration.md).
