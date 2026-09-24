/**
 * Epistemic Color Taxonomy (L1–L4)
 * Strictly enforces consistent epistemic color styling across all UI elements,
 * DAG nodes, badges, borders, and ECharts series/tooltips.
 */

export interface EpistemicLayerTheme {
  id: "L1" | "L2" | "L3" | "L4";
  name: string;
  badge: string;
  color: string; // hex
  lightBg: string;
  borderColor: string;
  textColor: string;
  glowColor: string;
}

export const EPISTEMIC_TAXONOMY: Record<"L1" | "L2" | "L3" | "L4", EpistemicLayerTheme> = {
  L1: {
    id: "L1",
    name: "Foundation & Ingestion",
    badge: "L1",
    color: "#3b82f6", // Blue
    lightBg: "rgba(59, 130, 246, 0.12)",
    borderColor: "rgba(59, 130, 246, 0.35)",
    textColor: "text-blue-500 dark:text-blue-400",
    glowColor: "rgba(59, 130, 246, 0.25)",
  },
  L2: {
    id: "L2",
    name: "Knowledge Graph",
    badge: "L2",
    color: "#10b981", // Green (Emerald)
    lightBg: "rgba(16, 185, 129, 0.12)",
    borderColor: "rgba(16, 185, 129, 0.35)",
    textColor: "text-emerald-500 dark:text-emerald-400",
    glowColor: "rgba(16, 185, 129, 0.25)",
  },
  L3: {
    id: "L3",
    name: "Argument Mining",
    badge: "L3",
    color: "#f59e0b", // Orange (Amber)
    lightBg: "rgba(245, 158, 11, 0.12)",
    borderColor: "rgba(245, 158, 11, 0.35)",
    textColor: "text-amber-500 dark:text-amber-400",
    glowColor: "rgba(245, 158, 11, 0.25)",
  },
  L4: {
    id: "L4",
    name: "TheoryNet & Fusion",
    badge: "L4",
    color: "#a855f7", // Purple
    lightBg: "rgba(168, 85, 247, 0.12)",
    borderColor: "rgba(168, 85, 247, 0.35)",
    textColor: "text-purple-500 dark:text-purple-400",
    glowColor: "rgba(168, 85, 247, 0.25)",
  },
};

export function getEpistemicLayerForPhase(phaseKey: string, ordinal?: number): "L1" | "L2" | "L3" | "L4" {
  const key = phaseKey.toLowerCase();
  if (key === "phase1" || ordinal === 1) return "L1";
  if (
    key === "phase2" ||
    key === "schema" ||
    key === "phase3" ||
    key === "phase3b" ||
    key === "phase4_maturation" ||
    ordinal === 2 ||
    ordinal === 3 ||
    ordinal === 4 ||
    ordinal === 5
  ) {
    return "L2";
  }
  if (key === "phase4" || key === "phase5" || ordinal === 6 || ordinal === 7) return "L3";
  if (key === "phase6" || key === "phase7" || key === "post" || key === "theorynet" || (ordinal && ordinal >= 8)) return "L4";
  return "L2";
}
