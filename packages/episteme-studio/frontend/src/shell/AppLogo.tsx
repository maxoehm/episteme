import React from "react";

export const AppLogo: React.FC = () => {
  return (
    <div className="flex items-center gap-1 select-none">
      <span className="font-mono text-xs text-app-heading font-medium tracking-tight">
        episteme
      </span>
      <span className="font-display text-xs text-app-muted font-normal tracking-tight">
        / studio
      </span>
    </div>
  );
};

