# [ISSUE-002] Multigraph Parallel Edge Encoding & Inter-Layer Projection Cones

| Metadata | Details |
| :--- | :--- |
| **Issue ID** | `ISSUE-002` |
| **Component(s)** | `packages/episteme-studio` (`frontend/src/graph/`) |
| **Roadmap Horizon** | **Horizon 1** (Platform Stabilization & Core Engine) |
| **Priority** | Low |
| **Status** | Open |
| **Source Ref** | [requirements_glp_project.md §1.1, §1.3](issues/shared/requirements_glp_project.md#L38-L72) |

---

## 1. Problem Statement & Motivation
In scientific and philosophical literature, identical entity or claim pairs frequently share multiple distinct epistemic connections simultaneously:
- An empirical co-occurrence edge (Layer 2) existing alongside a deductive entailment edge (Layer 3).
- Concurrent dialectical relations where a theory both `SUPPORTS` an empirical application under one condition while an edge in the opposite direction `CONSTRAINS` or `ATTACKS` it under another.

Currently, overlapping edges between the same two nodes can visually collapse or occlude each other in AntV G6. Additionally, while the studio supports toggling L1, L2, and L3 layers, there is no composite projection mode that visually draws "projection cones" linking high-level L3 theoretical nodes down to their grounding L2 entities and L1 source text chunks.

---

## 2. Functional Requirements
1. **Curved Parallel Multi-Edges**:
   - Update [`edgeStyling.ts`](packages/episteme-studio/frontend/src/graph/styling/edgeStyling.ts) to detect parallel edges $(u, v)_1, (u, v)_2, \dots$ between identical endpoints.
   - Automatically assign distinct curve offsets (`curveOffset: [20, -20, 40, -40, ...]`) to ensure concurrent edges remain individually legible, clickable, and hoverable.
   - Visually encode edge categories:
     - Empirical relations: solid stroke.
     - Theoretical/deductive links: dashed stroke.
     - Dialectical support/attack: polarity-colored arrows with distinct dash/solid patterns.
2. **Layer Composite Projection Mode (2.5D Cones)**:
   - When "Composite View" is active, render L3 nodes elevated with translucent visual cones or hulls projecting downwards to associated L2 entities and L1 chunks.
   - Selecting an L3 theory atom highlights its downstream epistemic justification footprint across L2 and L1.

---

## 3. Acceptance Criteria
- [ ] Nodes with multiple relationships between them display cleanly separated parallel curved arcs without visual occlusion.
- [ ] Each parallel edge can be independently selected or right-clicked to open [`EdgeContextMenu.tsx`](packages/episteme-studio/frontend/src/graph/EdgeContextMenu.tsx).
- [ ] Composite mode provides a clear visual hierarchy connecting theoretical claims to their underlying textual chunks.

---

## 4. Key Target Files
- [`packages/episteme-studio/frontend/src/graph/styling/edgeStyling.ts`](packages/episteme-studio/frontend/src/graph/styling/edgeStyling.ts)
- [`packages/episteme-studio/frontend/src/graph/GraphCanvas.tsx`](packages/episteme-studio/frontend/src/graph/GraphCanvas.tsx)
- [`packages/episteme-studio/frontend/src/graph/hooks/useG6Instance.ts`](packages/episteme-studio/frontend/src/graph/hooks/useG6Instance.ts)
