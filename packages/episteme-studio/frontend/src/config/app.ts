/**
 * Application metadata and configuration constants.
 * Single source of truth for branding, versioning, and environment details.
 */
export const APP_CONFIG = {
  name: "Episteme",
  title: "Episteme Studio",
  subtitle: "Theory Graph Workbench",
  description: "Theory Graph Analysis & Research Platform",
  version: `v${__APP_VERSION__}`,
  rawVersion: __APP_VERSION__,
  copyrightYear: new Date().getFullYear(),
} as const;
