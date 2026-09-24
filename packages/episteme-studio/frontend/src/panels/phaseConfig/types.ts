/**
 * Types and data models for Phase Configuration inspection and overlays.
 * Conforms to Interface Segregation Principle (ISP) with minimal, focused contracts.
 */

export type ConfigValueType = "string" | "number" | "boolean" | "array" | "object" | "null";

export interface PhaseConfigField {
  key: string;
  label: string;
  value: any;
  valueType: ConfigValueType;
  description?: string;
  unit?: string;
  badge?: string;
  defaultValue?: string | number | boolean;
  isAdvanced?: boolean;
  group?: "thresholds" | "limits" | "general";
}

export type PromptRole =
  | "direct"
  | "reasoning"
  | "format"
  | "gleaning"
  | "segmentation"
  | "linking"
  | "custom";

export interface PromptTemplateItem {
  id: string;
  name: string;
  role: PromptRole;
  template: string;
  variables: string[];
  description?: string;
}

export interface PhaseConfigDescriptor {
  phaseKey: string;
  phaseOrdinal: number;
  phaseName: string;
  description: string;
  category: string;
  parameters: PhaseConfigField[];
  prompts: PromptTemplateItem[];
  executionSettings: PhaseConfigField[];
  rawConfig: Record<string, any>;
}

export interface PhaseTabOption {
  key: string;
  ordinal: number;
  label: string;
  shortLabel: string;
  hasPrompts: boolean;
}
