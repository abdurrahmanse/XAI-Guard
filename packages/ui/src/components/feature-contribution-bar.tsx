import React from "react";

export interface FeatureContribution {
  feature: string;
  contribution: number;
  type: "push" | "pull";
}

export const FeatureContributionBar = ({ feature, contribution, type }: FeatureContribution) => {
  return (
    <div className="space-y-1">
      <div className="flex justify-between text-xs font-mono">
        <span>{feature}</span>
        <span className={type === 'push' ? "text-severity-critical" : "text-blue-400"}>
          {contribution > 0 ? "+" : ""}{contribution.toFixed(3)}
        </span>
      </div>
      <div className="h-1.5 w-full bg-secondary rounded-full overflow-hidden flex">
        <div className="w-1/2 flex justify-end">
          {type === 'pull' && (
            <div className="h-full bg-blue-500 rounded-l-full" style={{ width: `${Math.abs(contribution) * 300}%` }} />
          )}
        </div>
        <div className="w-1/2 flex justify-start">
          {type === 'push' && (
            <div className="h-full bg-severity-critical rounded-r-full" style={{ width: `${contribution * 300}%` }} />
          )}
        </div>
      </div>
    </div>
  );
};
