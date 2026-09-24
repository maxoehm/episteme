---
version: "alpha"
name: Epistemic IDE
description: Dual-mode scientific workspace engineered for topological graph inspection, high-density pipeline execution, and epistemic data modeling.
colors:
  primary: "#2563EB"
  primary-dark: "#3B82F6"
  canvas-light: "#FFFFFF"
  canvas-dark: "#09090B"
  surface-light: "#F8FAFC"
  surface-dark: "#18181B"
  surface-interactive-light: "#F1F5F9"
  surface-interactive-dark: "#27272A"
  rail-light: "#F8FAFC"
  rail-dark: "#111827"
  text-primary-light: "#0F172A"
  text-primary-dark: "#F8FAFC"
  text-muted-light: "#64748B"
  text-muted-dark: "#A1A1AA"
  border-subtle-light: "#E2E8F0"
  border-subtle-dark: "rgba(255, 255, 255, 0.08)"
  divider-light: "#E2E8F0"
  divider-dark: "rgba(255, 255, 255, 0.08)"
  state-success: "#059669"
  state-success-dark: "#10B981"
  graph-edge-light: "#94A3B8"
  graph-edge-dark: "#52525B"
  chart-grid-light: "rgba(15, 23, 42, 0.06)"
  chart-grid-dark: "rgba(255, 255, 255, 0.05)"
typography:
  h1:
    fontFamily: Manrope
    fontSize: 24px
    fontWeight: 600
    lineHeight: 32px
  h2:
    fontFamily: Manrope
    fontSize: 16px
    fontWeight: 500
    lineHeight: 24px
  body:
    fontFamily: Inter
    fontSize: 13px
    fontWeight: 400
    lineHeight: 18px
  body-tabular:
    fontFamily: Inter
    fontSize: 13px
    fontWeight: 500
    lineHeight: 18px
    fontFeature: '"tnum" 1'
  caption:
    fontFamily: Inter
    fontSize: 11px
    fontWeight: 400
    lineHeight: 14px
  mono:
    fontFamily: JetBrains Mono
    fontSize: 11px
    fontWeight: 400
    lineHeight: 16px
rounded:
  none: 0px
  sm: 4px
  md: 8px
  full: 9999px
spacing:
  compact-xs: 2px
  compact-sm: 4px
  sm: 8px
  md: 16px
  lg: 24px
components:
  canvas-workspace-light:
    backgroundColor: "{colors.canvas-light}"
    textColor: "{colors.text-primary-light}"
  canvas-workspace-dark:
    backgroundColor: "{colors.canvas-dark}"
    textColor: "{colors.text-primary-dark}"
  surface-panel-light:
    backgroundColor: "{colors.surface-light}"
    textColor: "{colors.text-primary-light}"
    rounded: "{rounded.md}"
    padding: "{spacing.md}"
  surface-panel-dark:
    backgroundColor: "{colors.surface-dark}"
    textColor: "{colors.text-primary-dark}"
    rounded: "{rounded.md}"
    padding: "{spacing.md}"
  rail-sidebar-light:
    backgroundColor: "{colors.rail-light}"
    textColor: "{colors.text-muted-light}"
    borderRight: "1px solid {colors.divider-light}"
    width: 280px
  rail-sidebar-dark:
    backgroundColor: "{colors.rail-dark}"
    textColor: "{colors.text-muted-dark}"
    borderRight: "1px solid {colors.divider-dark}"
    width: 280px
  dag-node-light:
    backgroundColor: "{colors.canvas-light}"
    textColor: "{colors.text-primary-light}"
    border: "1px solid {colors.border-subtle-light}"
    rounded: "{rounded.sm}"
    padding: "{spacing.sm}"
  dag-node-dark:
    backgroundColor: "{colors.surface-dark}"
    textColor: "{colors.text-primary-dark}"
    border: "1px solid {colors.border-subtle-dark}"
    rounded: "{rounded.sm}"
    padding: "{spacing.sm}"
  graph-edge-light:
    textColor: "{colors.graph-edge-light}"
  graph-edge-dark:
    textColor: "{colors.graph-edge-dark}"
  chart-container-light:
    backgroundColor: "{colors.surface-light}"
    textColor: "{colors.chart-grid-light}"
    border: "1px solid {colors.border-subtle-light}"
    rounded: "{rounded.md}"
    padding: "{spacing.md}"
  chart-container-dark:
    backgroundColor: "{colors.surface-dark}"
    textColor: "{colors.chart-grid-dark}"
    border: "1px solid {colors.border-subtle-dark}"
    rounded: "{rounded.md}"
    padding: "{spacing.md}"
  metric-tabular-display:
    typography: "{typography.body-tabular}"
    textColor: "{colors.text-primary-dark}"
  label-namespace-light:
    typography: "{typography.mono}"
    textColor: "{colors.text-muted-light}"
  label-namespace-dark:
    typography: "{typography.mono}"
    textColor: "{colors.text-muted-dark}"
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.canvas-light}"
    typography: "{typography.body}"
    rounded: "{rounded.sm}"
    padding: "{spacing.sm}"
  button-primary-dark:
    backgroundColor: "{colors.primary-dark}"
    textColor: "{colors.canvas-dark}"
    typography: "{typography.body}"
    rounded: "{rounded.sm}"
    padding: "{spacing.sm}"
  input-field-light:
    backgroundColor: "{colors.surface-interactive-light}"
    textColor: "{colors.text-primary-light}"
    border: "1px solid {colors.border-subtle-light}"
    typography: "{typography.body}"
    rounded: "{rounded.sm}"
    padding: "{spacing.sm}"
  input-field-dark:
    backgroundColor: "{colors.surface-interactive-dark}"
    textColor: "{colors.text-primary-dark}"
    border: "1px solid {colors.border-subtle-dark}"
    typography: "{typography.body}"
    rounded: "{rounded.sm}"
    padding: "{spacing.sm}"
  badge-success-light:
    backgroundColor: "{colors.surface-light}"
    textColor: "{colors.state-success}"
    border: "1px solid {colors.border-subtle-light}"
    typography: "{typography.caption}"
    rounded: "{rounded.full}"
    padding: "{spacing.compact-sm}"
  badge-success-dark:
    backgroundColor: "{colors.surface-dark}"
    textColor: "{colors.state-success-dark}"
    border: "1px solid {colors.border-subtle-dark}"
    typography: "{typography.caption}"
    rounded: "{rounded.full}"
    padding: "{spacing.compact-sm}"
---

## Overview

The Epistemic IDE design system approaches interface styling as an analytical instrument rather than consumer software (like Palantir Foundry, Linear, or Weights & Biases). The platform operates under a dual-theme paradigm where Light and Dark modes serve distinct operational objectives:

- **Dark Mode (Default Analytical Lens):** Formulated after executive operations consoles . It reduces cognitive fatigue during extended pipeline runs, minimizes display glare, and isolates attention on emitted luminescence (active nodes, status pills, and categorical graph marks).
- **Light Mode (High-Acuity Vector Lens):** Utilizes ambient reflection to maximize absolute edge sharpness when inspecting dense topological DAGs and overlapping categorical coordinates.

Both modes adhere to strict spatial density rules: information density takes precedence over decorative whitespace, while structural hierarchy is established through luminance and surface micro-elevation rather than visual clutter.

## Colors

Color functions as an operational state machine. Chromatic hues are strictly reserved for state signals, execution alerts, and categorical data marks. Backgrounds and containers use an inverted neutral hierarchy with symmetrical token mappings across themes:

- **Canvas (`#09090B` Dark / `#FFFFFF` Light):** Dark avoids pure black (`#000000`) to eliminate astigmatic halation; Light provides an unblemished, paper-crisp scientific ground.
- **Surface (`#18181B` Dark / `#F8FAFC` Light):** Elevated slate/off-white surface for primary modules, DAG inspector panels, and telemetry cards.
- **Surface Interactive (`#27272A` Dark / `#F1F5F9` Light):** Reactive fill for unbordered inputs, segmented track states, and hover transitions.
- **Rail (`#111827` Dark / `#F8FAFC` Light):** High-density panel background for pipeline stage trees and DAG navigators.
- **Hairline Dividers & Borders (`rgba(255, 255, 255, 0.08)` Dark / `#E2E8F0` Light):** Precise 1px structural rules establishing the architectural coordinate grid across both modes without drop shadows.
- **Text Hierarchy:**
  - *Dark Mode:* Primary readable content (`#F8FAFC`) at highest luminance, paired with muted machine metadata and configuration keys (`#A1A1AA`).
  - *Light Mode:* Primary readable content (`#0F172A`) for maximum optical acuity, paired with muted machine metadata (`#64748B`).
- **Vector & Chart Grid:** DAG topological connection edges use `#52525B` in Dark and `#94A3B8` in Light (minimum 1.5px stroke) to prevent anti-aliasing dropout. Cartographic coordinate gridlines utilize `rgba(255, 255, 255, 0.05)` (Dark) and `rgba(15, 23, 42, 0.06)` (Light).
- **Operational Blue (`#2563EB` / `#3B82F6`):** Active running state, pipeline execution triggers, and interactive focus indicators.
- **Success Emerald (`#059669` / `#10B981`):** Cache hits, verified epistemic artifacts, and healthy store states.

## Typography

Type selection enforces a strict boundary between structural framing, readable human semantics, and machine payloads.

- **Macro Structural Headers (Manrope):** Geometric sans-serif reserved exclusively for page titles (H1) and section heads (H2). Manrope provides geometric stability to large panels without crowding data spaces.
- **System Interface & Tabular Readouts (Inter):** Neo-grotesque standard for interface labels, tooltips, and data payloads. 
  - *Strict Rule:* All numerical statistics, execution runtimes, cache hit percentages, and matrix dimensions must enable tabular figures (`fontFeature: '"tnum" 1'`) to prevent horizontal jitter during live telemetry updates.
- **Machine Namespaces & Telemetry Logs (JetBrains Mono):** Reserved for configuration paths (e.g., `models.llm_model`), raw JSON payloads, run hash identifiers, and terminal execution traces.

## Layout

The viewport is organized into a persistent three-rail scientific cockpit:

1. **Left Navigation Rail (280px fixed):** Contains the pipeline hierarchy, run history, and topological stage tree. Demarcated by a continuous 1px vertical hairline divider (`border-right: 1px solid {colors.divider}`).
2. **Center Execution Inspector (Fluid):** Houses the active topological DAG canvas, output dataframes, KDE score density distributions, and framed document/report vitrines.
3. **Right Diagnostic Rail (340px fixed):** Displays real-time telemetry, cache blast-radius counters, and execution controls. Demarcated by a continuous 1px vertical hairline divider (`border-left: 1px solid {colors.divider}`).

### Architectural Grid & Stage Containment

- **Full-Height Hairline Grid:** Rather than floating cards or shadow breaks, the viewport is anchored to continuous 1px vertical and horizontal hairline rules. Every panel is an aligned compartment in a Cartesian drafting table.
- **Framed Stage Containment:** Central documents, DAG canvases, and reports sit inside framed stage cards featuring 1px hairline borders (`rounded.md`) with a dedicated top utility toolbar (pagination, zoom, export), producing the serene, contemplative focus of an exhibition vitrine or formal scientific report.

### Information Density Modes

The workspace supports two grid density profiles:

- **Comfortable Mode (Default):** 8px base spacing grid (`spacing.sm`) with 16px panel padding (`spacing.md`). Optimised for configuration editing and prompt synthesis.
- **Compact Mode (Analysis):** 4px base spacing grid (`spacing.compact-sm`) with collapsed margins and 11px micro-typography. Mandatory for multi-thousand node DAG traversals and epistemic relation tables.

## Elevation & Depth

Depth is defined through a universal **"Hairline Grid & Flat Containment"** doctrine across both modes:

- **Drop Shadows Prohibited:** Drop shadows are strictly prohibited in both themes—they create muddy halos against dark fields and introduce imprecise, floating consumer tropes in light mode.
- **Dark Mode ("Hairline Grid & Subtle Elevation" Doctrine):** Depth is achieved through a Cartesian grid of 1px semi-transparent hairline borders (`rgba(255, 255, 255, 0.08)`), reinforced by subtle background lightness shifts from `#09090B` (Canvas) to `#18181B` (Panels) to `#27272A` (Interactive surfaces). Modules never float; they reside within framed compartments.
- **Light Mode ("Divider-First & Monograph" Doctrine):** Flat elevation relies strictly on crisp 1px solid hairline borders (`#E2E8F0`) between functional regions, evoking Swiss editorial layout and academic scientific monographs. Surfaces transition quietly from `#FFFFFF` (Canvas) to `#F8FAFC` (Panels) to `#F1F5F9` (Interactive controls).
- **Overlay Shroud:** Modal inspectors and artifact previews apply a heavy backdrop filter blur (`backdrop-filter: blur(8px)`) with a `rgba(0, 0, 0, 0.7)` scrim (Dark) or `rgba(15, 23, 42, 0.3)` scrim (Light) to isolate complex pipelines beneath.

## Shapes

Shapes reflect utilitarian discipline:

- **Panels & Cards:** 8px border-radius (`rounded.md`) for primary modular containers and framed stage cards.
- **Controls & Nodes:** 4px border-radius (`rounded.sm`) for DAG nodes, text input bars, segmented toggles, and buttons.
- **Terminal & Logs:** 0px border-radius (`rounded.none`) flush against panel boundaries to maximize scannable terminal columns.
- **Pills & Status Indicators:** Fully rounded (`rounded.full`) for operational state badges (e.g., Cached, Running, Failed).

## Components

- **Framed Stage Card (Document / Inspector Vitrine):** Central stage container with 1px hairline border (`rounded.md`), integrated utility bar (`Page 1 / N`, zoom, actions), and generous internal breathing room to present complex artifacts with academic clarity.
- **DAG Node Card:** Defined by surface `#18181B` (Dark) / `#FFFFFF` (Light) on canvas `#09090B` / `#FFFFFF` with 4px border-radius, 1px subtle border, and 8px internal padding. Features an active left border highlight matching its operational state color.
- **Segmented Control (Thinking Level / Verbosity):** Dual-mode segmented pill track (e.g., `[Brief | Standard | Deep]`). In Dark Mode, a sunken container (`#111827`) housing pill segments where the active segment lifts to `#27272A` with an accented highlight and no harsh outlines. In Light Mode, a `#F1F5F9` container where the active segment lifts to `#FFFFFF` with a 1px `#E2E8F0` border.
- **Diagnostic KPI Tile:** High-luminance numerical readout utilizing `body-tabular` in `#F8FAFC` (Dark) / `#0F172A` (Light), paired with a micro-label (`caption`) in `#A1A1AA` / `#64748B` and an optional hairline micro-metric indicator bar.
- **Scientific Visualization Container:** Area charts (such as KDE distribution profiles) must render with a 15% opacity fill and a crisp 1.5px solid stroke. Gridlines must not compete with data lines, remaining pinned to `rgba(255, 255, 255, 0.05)` (Dark) and `rgba(15, 23, 42, 0.06)` (Light).
- **Telemetry Stream:** Monospaced terminal container utilizing `surface-dark` / `surface-light` with 1px boundary rules and syntax-highlighted status tokens (Emerald for `INFO`, Amber for `WARN`, Rose for `ERR`).

## Anti-Patterns & Key Architectural Learnings (Lessons from ConfigEditor)

During the iterative evolution of the workbench from legacy prototypes into the ROMER-inspired analytical console, five key anti-patterns and concrete design decisions were codified:

### 1. Shedding "Boxes Inside Boxes" (Box-Crate Syndrome)
- **The Failure Mode:** Stacking bordered card containers inside other bordered card containers (e.g. an upload button inside an bordered file list, inside an adder box, inside a parent card). This produces severe visual "jail bars" and heavy cognitive fatigue.
- **The Design Decision:** Use **Surface Washes & Hairline Separators** rather than bordered boxes.
  - Groups should use calm background fills (`bg-app-subtle/20` to `bg-app-subtle/40`) with 1px hairline horizontal dividers (`divide-y divide-app-border-subtle`).
  - Active list items receive an inset surface lift (`bg-app-subtle`) and an operational indicator dot (e.g. cyan or blue), not heavy multi-layered borders.

### 2. Typography Role Discipline: Sans-Serif vs. Monospace
- **The Failure Mode:** Using all-caps monospace (`font-mono uppercase tracking-wider`) for section titles (e.g. `GLOBAL STRUCTURAL ANCHOR`). This creates harsh, unstyled terminal aesthetic that reduces scannability.
- **The Design Decision:**
  - **Human Semantics & Section Heads:** Always use geometric sans-serif (**Manrope** `type-h1`, `type-h2`) in natural title/sentence case.
  - **Interface Labels & Captions:** Always use **Inter** (`type-body`, `type-caption`).
  - **Machine Payloads Only:** Strictly reserve **JetBrains Mono** (`type-mono`) for machine configuration keys (`structural_anchor.global_thesis`, `models.llm_model`), file paths, SHA hashes, and terminal outputs. Machine keys should sit as quiet, right-aligned captions, never primary section headings.

### 3. Eliminating Decorative "Ballast" Badges
- **The Failure Mode:** Placing decorative badges (like `[Coordinate System]`, `[Baseline Architecture]`, or `[Epistemic Ontology]`) right before section titles. They convey zero telemetry, duplicate the title, and clutter the eye.
- **The Design Decision:** Remove decorative badges entirely. Badges/pills are operational state signals only (e.g., `Cached`, `Recompute`, `Active`, `Skip`). If a category is necessary, display it as a quiet, muted micro-caption (`type-caption text-app-muted font-mono uppercase tracking-wider`).

### 4. Sub-Tabbed Scoping vs. Endless Scroll-Dumps
- **The Failure Mode:** Stacking multiple distinct domain workflows (e.g. candidate document uploads, global prompt coordinates, and run manifest metadata) onto a single 2,000px vertical scroll view.
- **The Design Decision:** Divide high-density configuration workspaces into **Zero-Box Segmented Sub-Tabs** (e.g. `[Primary Sources]` | `[Structural Anchors]` | `[Run Metadata]`). This isolates cognitive focus, provides generous vertical space for multiline inputs (thesis, outlines, prompt editors), and preserves visual calm.

### 5. Single Source of Truth for Controls & Toolbars
- **The Failure Mode:** Displaying duplicate target/profile selectors or execution mode indicators in both a global top header and an internal card utility bar.
- **The Design Decision:** Never stack pseudo-toolbars. Elevate top-level scoping parameters (Target Document, Execution Scope, Profile, Discard Overrides) to the persistent plane header ([`StageScopeHeader`](packages/glp-studio/frontend/src/panels/configEditor/components/StageScopeHeader.tsx)). Allow the central canvas content to breathe as an unboxed, direct workspace.

### 6. Quiet Rest States & Hover-Discovered Affordances
- **The Failure Mode:** Showing permanent high-contrast drag handles (`GripVertical`), action menus (`...`), and heavy borders on every inactive item in long lists.
- **The Design Decision:** Inactive items in navigation rails and stage lists should be borderless text rows in their rest state (`text-app-text hover:bg-app-subtle/50`). Drag handles and secondary menus must be visually muted or revealed on hover (`opacity-0 group-hover:opacity-100`), keeping the ambient baseline quiet and contemplative.

### 7. The "Floating Island" Anti-Pattern vs. Edge-to-Edge Docked Panes
- **The Failure Mode:** Placing a centered, rounded white card (`max-w-4xl mx-auto p-6 rounded-[8px] border shadow-xs`) inside an ocean of pale grey (`bg-[#F8FAFC]`). This creates arbitrary margins, destroys structural depth, and makes analytical tools resemble generic administrative SaaS settings pages.
- **The Design Decision:** High-performance research workbenches (Cursor, Linear, Datadog) use an **Edge-to-Edge Docked Layout** (`flex-1 flex flex-col min-w-0 bg-white dark:bg-app-bg overflow-hidden`).
  - Panels dock flush against 1px hairline borders (`#E2E8F0` / dark `border-app-border`) with `0px` outer margins.
  - Data grids and terminal streams run edge-to-edge from the toolbar to the bottom rail.
  - Framed stage cards (`rounded.md`) are strictly reserved for discrete document/report vitrines (like PDF readers or Markdown previews), never data tables or configuration grids.

### 8. Dual-Navigation Hierarchy Trap (IDE Navigation Model)
- **The Failure Mode:** Placing top horizontal sub-tabs directly adjacent to or above a hierarchical left rail tree. This creates confusion over which control drives view state, duplicates active indicators, and squanders vertical canvas space.
- **The Design Decision:** Enforce a strict **Single-Controller IDE Navigation Model**:
  - The **Left Rail Tree** is the primary, definitive hierarchical navigator.
  - The horizontal sub-header toolbar (fixed 44px) must be a **Contextual Action Bar**, never a duplicate navigation bar. It is strictly reserved for:
    1. Contextual breadcrumbs (`Epistemic Ontology / Entity Types`)
    2. Quantitative scope count pills (`9 types`, `18 relations`, `15 pending`)
    3. Keyboard shortcut hints (`[j] [k] to navigate`)
    4. Fast text search/filter input (`Filter rows...`)
    5. Contextual primary actions (`+ Add Entity`, `+ Add Relation`, `+ Add Component`, `+ Add Alias`)
    6. System commit triggers (`Rescan`, `Save`)

### 9. Modern High-Density Data Grid Specification (Linear/Retool Model)
- **The Failure Mode:** Rendering data tables with raw unstyled borders, generic body fonts for machine keys, inline adder rows that distort column alignment, or missing column headers.
- **The Design Decision:** Standardize data tables using the **Headless Linear-Style Data Grid**:
  - **Table Headers:** Background `surface-light` (`#F8FAFC`) / `surface-dark` (`#18181B`), border-b `1px solid divider`, Inter 11px, weight 600, uppercase, `tracking-[0.05em]`, text `muted` (`#64748B` / `#A1A1AA`). Column headers must support click-to-sort with subtle chevrons.
  - **Table Rows:** Fixed height `40px` (`h-10`), padding `0 24px` (`px-6`).
  - **Row States:** Active row receives an inset background wash (`#F1F5F9` / `bg-app-subtle`) with a solid `2px` left border in primary blue (`#2563EB`) and no outer double borders. Inactive rows: `border-transparent hover:bg-[#F8FAFC] dark:hover:bg-app-subtle/50`.
  - **Typography Roles in Data Cells:**
    - Machine Identifiers / Predicates: JetBrains Mono 12px, weight 500, `#0F172A` (Dark: `#F8FAFC`).
    - Human Prose / Prompt Guidance: Inter 13px, weight 400, leading-normal, text muted (`#64748B` / `#A1A1AA`).
    - Numerical Metrics / Counts: Tabular numbers (`fontFeature: '"tnum" 1'`), right-aligned.
    - Formal Properties / Polarities / Status: Micro-badges with 10px monospace text and 20% opacity border tinted by operational state.
  - **Add Row Actions:** Moved out of the table body to the sub-header toolbar or panel header as a clean secondary button (`+ Add Entity`), keeping the grid pure data display.

### 10. Scientific Structural Telemetry vs. Generic KPI Cards
- **The Failure Mode:** Placing 4 generic SaaS progress-bar cards with arbitrary percentages and colored horizontal lines in inspector sidebars. They convey zero topological depth.
- **The Design Decision:** Replace superficial cards with **High-Density Structural Telemetry Tables**:
  - Structured key-value rows displaying formal epistemic graph invariants: *Topological Sparsity*, *DAG Acyclicity (Strict DAG)*, *Dialectical Balance (% Supp / % Atk)*, *Contradiction Rate*, and *Open-Vocabulary Drift*.
  - Paired with an **Ontological Distribution Summary Bar** displaying exact entity-to-relation class proportions.

### 11. Keyboard-First Triage Ergonomics
- **The Failure Mode:** Requiring mouse clicks to inspect every individual entity, relation, or unmapped candidate in long lists.
- **The Design Decision:** All analytical master-detail workbenches must support rapid keyboard triage:
  - Standard `j` / `k` (or `ArrowDown` / `ArrowUp`) traversal to step through active rows.
  - Immediate, reactive synchronization of the Contextual Inspector rail as selection advances.
  - Automatic bypass of keyboard listeners when focus is inside text fields (`input`, `textarea`, `select`).

## Do's and Don'ts

### Do's
- **Do** anchor layouts to 1px hairline dividers and vertical rules in both Dark and Light modes to maintain an architectural, contemplative grid.
- **Do** dock data tables and canvases edge-to-edge with 0px outer margins against panel boundaries.
- **Do** use the left rail as the single source of truth for hierarchical navigation, keeping the 44px toolbar strictly for breadcrumbs, counts, search, and actions.
- **Do** maintain complete token symmetry between Dark Mode (analytical operations console) and Light Mode (academic scientific monograph).
- **Do** enforce tabular numeral settings (`tnum`) across all runtime numbers, data matrix coordinates, and percentage indicators.
- **Do** format table rows with fixed 40px height, inset active surface washes, and solid 2px left blue borders.
- **Do** support keyboard traversal (`j`/`k`, arrow keys) in master-detail list views with immediate inspector synchronization.
- **Do** display high-density key-value structural telemetry for graph invariants rather than generic SaaS metric cards.
- **Do** calibrate categorical chart hues to pass WCAG AA (4.5:1 minimum) contrast against both `#09090B` and `#FFFFFF`.
- **Do** thicken DAG vector edges to at least 1.5px (`#52525B` in Dark, `#94A3B8` in Light) to mitigate anti-aliasing degradation.
- **Do** style custom scrollbars to match elevated panel colors (`#27272A` / `#E2E8F0`) to prevent glaring OS scrollbars.
- **Do** reserve JetBrains Mono strictly for code, namespaces, file paths, and telemetry values.

### Don'ts
- **Don't** use drop shadows in *either* Dark or Light mode; structural depth is established exclusively via 1px hairline dividers, subtle surface lightness shifts, and flat containment.
- **Don't** trap data grids inside floating cards surrounded by oceans of gray canvas padding ("Floating Island" problem).
- **Don't** create competing dual-navigation tabs above an already-present hierarchical left rail tree.
- **Don't** nest boxes inside boxes; group peer items using quiet background surface washes and hairline divider lines (`divide-y divide-app-border-subtle`).
- **Don't** use inline editable table rows to add new items that distort fixed data column alignments; use clean modal dialogs.
- **Don't** use pure black (`#000000`) with pure white (`#FFFFFF`) text, as the extreme luminance difference causes visual halation and astigmatic eye fatigue.
- **Don't** use uppercase monospace for readable human section titles; use Manrope or Inter with natural casing.
- **Don't** add decorative badges before titles that do not communicate live operational state.
- **Don't** duplicate controls between persistent plane headers and child content cards.
- **Don't** introduce generic, fluffy whitespace paddings in data areas; every visual element must prioritize high signal-to-noise density.
- **Don't** use Manrope for tabular or numerical payloads; geometric sans figures do not align in high-density data matrices.