import React from "react";
import { Network, Target, Activity, BrainCircuit } from "lucide-react";

interface ThreatCoreInfoProps {
  sourceIp: string;
  destinationIp: string;
  attackType: string;
  confidence: number;
}

export const ThreatCoreInfo = ({ sourceIp, destinationIp, attackType, confidence }: ThreatCoreInfoProps) => {
  return (
    <div className="grid grid-cols-2 gap-4 p-4 bg-card border rounded-lg shadow-sm">
      <div className="space-y-1">
        <span className="text-xs text-muted-foreground flex items-center gap-1"><Network className="w-3 h-3"/> Source</span>
        <p className="font-mono text-sm">{sourceIp}</p>
      </div>
      <div className="space-y-1">
        <span className="text-xs text-muted-foreground flex items-center gap-1"><Target className="w-3 h-3"/> Destination</span>
        <p className="font-mono text-sm">{destinationIp}</p>
      </div>
      <div className="space-y-1">
        <span className="text-xs text-muted-foreground flex items-center gap-1"><Activity className="w-3 h-3"/> Classification</span>
        <p className="font-medium text-sm">{attackType}</p>
      </div>
      <div className="space-y-1">
        <span className="text-xs text-muted-foreground flex items-center gap-1"><BrainCircuit className="w-3 h-3"/> Confidence</span>
        <p className="font-medium text-sm">{(confidence * 100).toFixed(1)}%</p>
      </div>
    </div>
  );
};
