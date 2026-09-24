# Episteme: Theory Graph Language Pipeline

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/downloads/release/python-3130/)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)

**Episteme** is a state-of-the-art framework and research library for constructing and evaluating **Theory Graphs** from German and English scientific literature.

Unlike traditional knowledge graphs that primarily extract isolated factual triples (e.g. `(Einstein, BornIn, Ulm)`), **Theory Graphs** capture the inferential, axiomatic, and argumentative structures that define formal scientific paradigms (e.g., core theoretical hypotheses, empirical observation sentences, correspondence laws, and defeasible attack/support relations).

---

## Architecture Overview

Episteme implements a multi-layer architecture spanning document text, empirical knowledge graphs, and model-theoretic theory nets:

* **Layer 1 (Provenance & Source Embedding)**: Verbatim document chunks, character-level offsets, and structural Table-of-Contents anchors.
* **Layer 2 (Domain Knowledge Graph)**: Entity resolution, co-reference resolution, and localized relation extraction.
* **Layer 3 (Theory Framework & Argument Mining)**: Argument components (premises, claims), epistemic justifications ($J$), and theory-net topologies.

### Monorepo Layout

```
episteme/
├── packages/
│   ├── episteme-pipeline/   # Core multi-phase extraction engine
│   ├── epistemetrics/       # Standalone formal theory-graph evaluation suite
│   └── episteme-studio/     # Run-oriented workbench (FastAPI + React/TypeScript)
├── docs/                    # Comprehensive documentation
├── issues/                  # Structured engineering backlog & specifications
├── paper/                   # Academic publication sources (PNAS Nexus format)
├── pyproject.toml           # Root workspace configuration
└── zensical.toml            # Documentation site configuration
```

---

## Quickstart

### Prerequisites
* Python 3.13+
* [`uv`](https://docs.astral.sh/uv/) package manager
* Optional: Neo4j 5.x+ instance (with Graph Data Science plugin)

### Installation

```bash
# Clone the repository
git clone https://github.com/maoem/network-construct.git
cd network-construct

# Sync workspace dependencies
uv sync
```

### Running the Pipeline

```bash
# Run the pipeline with default configuration
uv run python -m pipeline.runtime.runner --input examples/text/sample.md
```

### Launching GLP Studio

```bash
# Start backend API and frontend
uv run python -m glp_studio
```

---

## Documentation

Full documentation is available in the `docs/` directory or can be served locally:

```bash
uv run zensical serve
```

---

## Citation & License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

If you use Episteme in your research, please cite:

```bibtex
@article{episteme_2026,
  title={Episteme: A Synergized Bidirectional Reasoning Engine for Scientific Theory Graphs},
  author={Maoem},
  year={2026}
}
```
