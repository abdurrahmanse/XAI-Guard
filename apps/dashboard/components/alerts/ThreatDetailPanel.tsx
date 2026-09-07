"use client";

import React from "react";
import { Sheet, SheetContent, SheetHeader, SheetTitle, SheetDescription } from "@/components/ui/sheet";
import { useAlertsStore } from "@/stores/alerts-store";
import { ShieldAlert, Activity, Target, Network, BrainCircuit } from "lucide-react";

export const ThreatDetailPanel = () => {
  const selectedAlert = useAlertsStore((state) => state.selectedAlert);
  const setSelectedAlert = useAlertsStore((state) => state.setSelectedAlert);

  // Mock SHAP data for demonstration. In prod, this would fetch from GET /v1/explanations
  const mockShapData = [
    { feature: "Flow_Duration", contribution: 0.15, type: "push" },
    { feature: "Fwd_Packet_Length_Max", contribution: 0.12, type: "push" },
    { feature: "Bwd_Packet_Length_Std", contribution: 0.08, type: "push" },
    { feature: "Init_Win_bytes_forward", contribution: -0.05, type: "pull" },
  ];

  return (
    <Sheet open={!!selectedAlert} onOpenChange={(open) => !open && setSelectedAlert(null)}>
      <SheetContent className="w-full sm:max-w-md lg:max-w-lg xl:max-w-xl overflow-y-auto">
        {selectedAlert && (
          <div className="space-y-6">
            <SheetHeader>
              <div className="flex items-center gap-2 mb-2">
                <ShieldAlert className="w-5 h-5 text-severity-critical" />
                <SheetTitle className="text-xl">Threat Details</SheetTitle>
              </div>
              <SheetDescription className="font-mono text-xs">
                ID: {selectedAlert.id}
              </SheetDescription>
            </SheetHeader>

            {/* Core Info */}
            <div className="grid grid-cols-2 gap-4 p-4 bg-card border rounded-lg shadow-sm">
              <div className="space-y-1">
                <span className="text-xs text-muted-foreground flex items-center gap-1"><Network className="w-3 h-3"/> Source</span>
                <p className="font-mono text-sm">{selectedAlert.source_ip}</p>
              </div>
              <div className="space-y-1">
                <span className="text-xs text-muted-foreground flex items-center gap-1"><Target className="w-3 h-3"/> Destination</span>
                <p className="font-mono text-sm">{selectedAlert.destination_ip}</p>
              </div>
              <div className="space-y-1">
                <span className="text-xs text-muted-foreground flex items-center gap-1"><Activity className="w-3 h-3"/> Classification</span>
                <p className="font-medium text-sm">{selectedAlert.attack_type}</p>
              </div>
              <div className="space-y-1">
                <span className="text-xs text-muted-foreground flex items-center gap-1"><BrainCircuit className="w-3 h-3"/> Confidence</span>
                <p className="font-medium text-sm">{(selectedAlert.confidence * 100).toFixed(1)}%</p>
              </div>
            </div>

            {/* MITRE Mapping */}
            <div className="space-y-3">
              <h4 className="text-sm font-semibold uppercase tracking-wider text-muted-foreground">MITRE ATT&CK Mapping</h4>
              <div className="p-4 rounded-lg bg-accent/50 border flex flex-col gap-2">
                <div className="flex items-center gap-2">
                  <span className="px-2 py-1 text-xs font-bold bg-blue-500/20 text-blue-400 border border-blue-500/30 rounded">
                    {selectedAlert.mitre_technique_id || "T1499.001"}
                  </span>
                  <span className="text-sm font-medium">Endpoint Denial of Service</span>
                </div>
                <p className="text-xs text-muted-foreground">
                  Adversaries may perform endpoint denial of service (DoS) attacks to degrade or block the availability of services.
                </p>
              </div>
            </div>

            {/* SHAP Explanation */}
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <h4 className="text-sm font-semibold uppercase tracking-wider text-muted-foreground">XAI Explanation (SHAP)</h4>
                <span className="text-[10px] bg-white/10 px-2 py-0.5 rounded-full">XGBoost v2.1</span>
              </div>
              <div className="space-y-4 p-4 border rounded-lg bg-card/50">
                <p className="text-xs text-muted-foreground">
                  Features pushing the model towards {selectedAlert.attack_type} (Red) vs towards BENIGN (Blue).
                </p>
                
                <div className="space-y-3">
                  {mockShapData.map((f, i) => (
                    <div key={i} className="space-y-1">
                      <div className="flex justify-between text-xs font-mono">
                        <span>{f.feature}</span>
                        <span className={f.type === 'push' ? "text-severity-critical" : "text-blue-400"}>
                          {f.contribution > 0 ? "+" : ""}{f.contribution.toFixed(3)}
                        </span>
                      </div>
                      <div className="h-1.5 w-full bg-secondary rounded-full overflow-hidden flex">
                        {/* Fake zero-axis center visualization */}
                        <div className="w-1/2 flex justify-end">
                          {f.type === 'pull' && (
                            <div className="h-full bg-blue-500 rounded-l-full" style={{ width: `${Math.abs(f.contribution) * 300}%` }} />
                          )}
                        </div>
                        <div className="w-1/2 flex justify-start">
                          {f.type === 'push' && (
                            <div className="h-full bg-severity-critical rounded-r-full" style={{ width: `${f.contribution * 300}%` }} />
                          )}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>

          </div>
        )}
      </SheetContent>
    </Sheet>
  );
};
