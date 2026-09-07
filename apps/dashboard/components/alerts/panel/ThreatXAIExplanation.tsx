import React from "react";
import { FeatureContributionBar, type FeatureContribution } from "@xaiguard/ui";

interface ThreatXAIExplanationProps {
  attackType: string;
  contributions: FeatureContribution[];
}

export const ThreatXAIExplanation = ({ attackType, contributions }: ThreatXAIExplanationProps) => {
  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between">
        <h4 className="text-sm font-semibold uppercase tracking-wider text-muted-foreground">XAI Explanation (SHAP)</h4>
        <span className="text-[10px] bg-white/10 px-2 py-0.5 rounded-full">XGBoost v2.1</span>
      </div>
      <div className="space-y-4 p-4 border rounded-lg bg-card/50">
        <p className="text-xs text-muted-foreground">
          Features pushing the model towards {attackType} (Red) vs towards BENIGN (Blue).
        </p>
        
        <div className="space-y-3">
          {contributions.map((f, i) => (
            <FeatureContributionBar key={i} {...f} />
          ))}
        </div>
      </div>
    </div>
  );
};
