import React from "react";

export const MitreBadge = ({ techniqueId, title, description }: { techniqueId: string, title: string, description: string }) => {
  return (
    <div className="p-4 rounded-lg bg-accent/50 border flex flex-col gap-2">
      <div className="flex items-center gap-2">
        <span className="px-2 py-1 text-xs font-bold bg-blue-500/20 text-blue-400 border border-blue-500/30 rounded">
          {techniqueId}
        </span>
        <span className="text-sm font-medium">{title}</span>
      </div>
      <p className="text-xs text-muted-foreground">{description}</p>
    </div>
  );
};
