# ADR 0008: Diátaxis Documentation Framework

## Status

Accepted

## Context

Our documentation has grown organically over time, resulting in:

- Inconsistent structure and organization
- Mixed content types (tutorials mixed with reference, theory mixed with implementation)
- Difficulty for users to find what they need
- Challenges for maintainers in adding new content consistently

We need a systematic approach to documentation that:

1. Serves different user needs (researchers, developers, reviewers)
2. Provides clear organization and navigation
3. Is sustainable for long-term maintenance
4. Supports our dual mandate (research + engineering)

## Decision

We adopt the **Diátaxis Framework** as our documentation methodology.

### What is Diátaxis?

Diátaxis (from Ancient Greek δῐᾰ́τᾰξῐς: dia "across" + taxis "arrangement") is a systematic approach to technical
documentation that identifies four distinct user needs and corresponding documentation forms:

1. **Tutorials** - Learning-oriented
    - Purpose: Onboarding and skill-building
    - Audience: New users
    - Example: "Building your first theory graph"

2. **How-To Guides** - Goal-oriented
    - Purpose: Solving specific problems
    - Audience: Users working on tasks
    - Example: "How to configure Neo4j connection"

3. **Technical Reference** - Information-oriented
    - Purpose: Looking up facts and specifications
    - Audience: Users needing precise information
    - Example: API documentation, phase contracts

4. **Explanation** - Understanding-oriented
    - Purpose: Providing context and background
    - Audience: Users seeking deeper understanding
    - Example: Mathematical models, epistemological foundations

### Our Implementation

We've adapted Diátaxis for our research-engineering hybrid project:

```
docs/
├── getting_started/      # Tutorials + onboarding How-To guides
├── tutorials/            # Complete learning workflows
├── how_to/              # Task-specific guides
├── concepts/            # Explanation (theory, mathematics, epistemology)
├── workflow/            # Explanation + How-To (implementation details)
├── reference/           # Technical Reference (API, schemas, contracts)
├── research/            # Explanation (evaluation methodology, validation)
├── experiments/         # Explanation (empirical results, observations)
├── observability/       # How-To + Reference (events, monitoring)
├── adr/                 # Explanation (architectural decisions)
└── architecture/        # Explanation (system design, patterns)
```

### Research Adaptation

For our research project, we've enhanced the framework:

- **Theory & Concepts** (Explanation): Mathematical models, epistemological justifications
- **Pipeline Implementation** (How-To + Explanation): Code-level implementation details
- **Architecture & Decisions** (Explanation): Technical choices and rationale
- **Research & Evaluation** (Explanation): Validation methodology and results

## Consequences

### Positive

1. **Clear user pathways**: Each documentation type serves a specific need
2. **Reduced cognitive load**: Users find what they need faster
3. **Easier maintenance**: New content has a clear home
4. **Improved quality**: Each type has distinct writing guidelines
5. **Research transparency**: Theory is separated from implementation

### Negative

1. **Migration effort**: Existing content needs reorganization
2. **Learning curve**: Contributors must understand the framework
3. **Potential over-structuring**: Some content may not fit cleanly

### Mitigations

1. **Index pages**: Each section has clear navigation and cross-references
2. **Documentation**: This ADR explains the framework
3. **Flexibility**: The framework guides but doesn't constrain

## Alternatives Considered

1. **Traditional API-first documentation**
    - Would favor engineers over researchers
    - Doesn't support our dual mandate

2. **Academic paper structure**
    - Too theoretical for developers
    - Doesn't support reproducibility

3. **Ad-hoc organization** (current state)
    - Proven to cause confusion
    - Scales poorly

## References

- [Diátaxis Framework](https://diataxis.fr/) - Official documentation
- Diátaxis, from the Ancient Greek δῐᾰ́τᾰξῐς: dia ("across") and taxis ("arrangement")
- Solves problems related to documentation content (what to write), style (how to write it) and architecture (how to
  organise it)

## Related ADRs

- [ADR 0001: Neo4j Async Graph Backend](0001-neo4j-async-graph-backend.md)
- [ADR 0005: Two-Pass Fusion Strategy](0005-two-pass-fusion-strategy.md)

## Implementation Date

2026-06-23
