/**
 * Types and contracts for the Engine Settings panel and Contextual Inspector.
 */

export type SelectedItemType = "node" | "relation" | "component" | "arg_relation" | "unmapped_predicate" | "alias";

export interface SelectedItem {
  type: SelectedItemType;
  id: string;
}

/**
 * Demo Data Contract: Schema Validation Rule
 * Used by DemoValidationRules subcomponent.
 */
export interface DemoValidationRule {
  id: string;
  ruleName: string;
  description: string;
  severity: "error" | "warning" | "info";
  enabled: boolean;
}

/**
 * Demo Data Contract: Schema Audit History Entry
 * Used by DemoEditHistory subcomponent.
 */
export interface DemoAuditHistoryEntry {
  id: string;
  timestamp: string;
  author: string;
  changeSummary: string;
  version: string;
}
