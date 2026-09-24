export interface ProgressionSnapshot {
  step: number;
  count: number;
  scores: number[];
  mean: number;
  timestamp: string;
}

/**
 * Pure function to calculate progression snapshots for confidence scores at a given step interval.
 *
 * @param rawScores - Array of floating point confidence scores [0..1]
 * @param interval - Interval count for capturing discrete progression snapshots
 * @returns Array of snapshots from first interval to completion
 */
export function calculateProgressionSnapshots(
  rawScores: number[],
  interval: number = 20
): ProgressionSnapshot[] {
  if (!rawScores) {
    return [];
  }
  // Reject malformed streamed values (NaN/Infinity/strings) so snapshots never
  // carry non-finite scores into the replay/KDE render path.
  const validScores = rawScores.filter((s) => typeof s === "number" && Number.isFinite(s));
  if (validScores.length === 0) {
    return [];
  }
  const effectiveInterval = Math.max(1, interval);
  const snapshots: ProgressionSnapshot[] = [];
  for (let i = effectiveInterval; i <= validScores.length; i += effectiveInterval) {
    const slice = validScores.slice(0, i);
    const mean = slice.reduce((a, b) => a + b, 0) / slice.length;
    snapshots.push({
      step: Math.floor(i / effectiveInterval),
      count: i,
      scores: slice,
      mean: Math.round(mean * 1000) / 1000,
      timestamp: new Date().toISOString(),
    });
  }
  // Include terminal snapshot if there are leftover points or none captured yet
  if (validScores.length > 0 && (snapshots.length === 0 || snapshots[snapshots.length - 1].count < validScores.length)) {
    const mean = validScores.reduce((a, b) => a + b, 0) / validScores.length;
    snapshots.push({
      step: snapshots.length + 1,
      count: validScores.length,
      scores: [...validScores],
      mean: Math.round(mean * 1000) / 1000,
      timestamp: new Date().toISOString(),
    });
  }
  return snapshots;
}
