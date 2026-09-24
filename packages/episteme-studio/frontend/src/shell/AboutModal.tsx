import React from "react";
import {Scale, X} from "lucide-react";
import {APP_CONFIG} from "@/config/app";

interface AboutModalProps {
    isOpen: boolean;
    onClose: () => void;
}

export const AboutModal: React.FC<AboutModalProps> = ({isOpen, onClose}) => {
    if (!isOpen) return null;

    return (
        <div
            className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-xs p-4 animate-in fade-in duration-150">
            <div
                className="w-full max-w-lg bg-app-surface border border-app-border rounded-xl shadow-2xl overflow-hidden flex flex-col text-xs text-app-text select-none animate-in zoom-in-95 duration-150"
                onClick={(e) => e.stopPropagation()}
            >
                {/* Header */}
                <div className="flex items-center justify-between px-5 py-3 border-b border-app-border bg-app-surface">
                    <div className="flex items-center gap-2.5">
                        <div
                            className="flex items-center justify-center w-7 h-7 rounded-lg bg-blue-500/10 border border-blue-500/20 text-blue-600 dark:text-blue-400">
                            <Scale className="w-4 h-4"/>
                        </div>
                        <div>
                            <h3 className="font-semibold text-app-heading text-sm leading-tight">
                                {APP_CONFIG.title}
                            </h3>
                            <span className="font-mono text-[10px] text-app-muted">
                {APP_CONFIG.version} · {APP_CONFIG.subtitle}
              </span>
                        </div>
                    </div>
                    <button
                        onClick={onClose}
                        className="p-1 rounded-md text-app-muted hover:text-app-heading hover:bg-app-subtle transition-colors cursor-pointer"
                        title="Close"
                    >
                        <X className="w-4 h-4"/>
                    </button>
                </div>

                {/* Content Body */}
                <div className="p-5 space-y-4 overflow-y-auto max-h-[70vh] text-xs leading-relaxed select-text">
                    {/* Abstract / Description */}
                    <p className="text-app-text">
                        <strong>Episteme</strong> is an extensible pipeline and interactive visual workbench for
                        constructing, evaluating, and exploring multi-layered theory graphs from scientific literature.
                    </p>

                    {/* Legal & Licensing */}
                    <div className="space-y-1.5 pt-1 border-t border-app-border-subtle">
                        <div className="flex items-center justify-between text-[11px]">
                            <span className="font-semibold text-app-heading">License</span>
                            <span
                                className="font-mono text-[10px] px-1.5 py-0.5 rounded bg-blue-500/10 text-blue-600 dark:text-blue-400 border border-blue-500/20 font-medium">
                MIT License
              </span>
                        </div>
                        <p className="text-[11px] text-app-muted leading-relaxed">
                            Open-source software provided under the MIT License. Permitted for academic research,
                            extension, and commercial application with attribution.
                        </p>
                    </div>

                    {/* Architecture & Tech Stack */}
                    <div className="space-y-1.5 pt-1 border-t border-app-border-subtle">
                        <div className="flex items-center gap-1.5 font-semibold text-app-heading text-[11px]">
                            <span>Engine & Dependencies</span>
                        </div>
                        <ul className="grid grid-cols-2 gap-2 text-[11px] text-app-muted list-disc list-inside">
                            <li>Graph Engine: Neo4j & AntV G6</li>
                            <li>Backend: FastAPI & Python uv</li>
                            <li>Frontend: React 18 & Vite, ECharts, Zustand, TanStack and TailwindCSS</li>
                        </ul>
                    </div>
                </div>

                {/* Footer */}
                <div
                    className="px-5 py-2.5 border-t border-app-border bg-app-surface flex items-center justify-between text-[11px] text-app-muted shrink-0">
                    <span className="font-mono text-[10px]">© {APP_CONFIG.copyrightYear} Episteme Research</span>
                    <button
                        onClick={onClose}
                        className="px-3 py-1 rounded bg-app-heading text-app-surface font-medium hover:opacity-90 transition-opacity cursor-pointer text-xs"
                    >
                        Close
                    </button>
                </div>
            </div>
        </div>
    );
};
