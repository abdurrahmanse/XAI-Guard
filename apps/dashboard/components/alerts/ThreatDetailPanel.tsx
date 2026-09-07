"use client";

import React from "react";
import { Sheet, SheetContent, SheetHeader, SheetTitle, SheetDescription } from "@/components/ui/sheet";
import { useAlertsStore } from "@/stores/alerts-store";
import { ShieldAlert } from "lucide-react";
import { MitreBadge } from "@xaiguard/ui";
import { ThreatCoreInfo } from "./panel/ThreatCoreInfo";
import { ThreatXAIExplanation } from "./panel/ThreatXAIExplanation";

export const ThreatDetailPanel = () => {
  const selectedAlert = useAlertsStore((state) => state.selectedAlert);
  const setSelectedAlert = useAlertsStore((state) => state.setSelectedAlert);

  const mockShapData = [
    { feature: "Flow_Duration", contribution: 0.15, type: "push" as const },
    { feature: "Fwd_Packet_Length_Max", contribution: 0.12, type: "push" as const },
    { feature: "Bwd_Packet_Length_Std", contribution: 0.08, type: "push" as const },
    { feature: "Init_Win_bytes_forward", contribution: -0.05, type: "pull" as const },
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

            <ThreatCoreInfo 
              sourceIp={selectedAlert.source_ip}
              destinationIp={selectedAlert.destination_ip}
              attackType={selectedAlert.attack_type}
              confidence={selectedAlert.confidence}
            />

            <div className="space-y-3">
              <h4 className="text-sm font-semibold uppercase tracking-wider text-muted-foreground">MITRE ATT&CK Mapping</h4>
              <MitreBadge 
                techniqueId={selectedAlert.mitre_technique_id || "T1499.001"}
                title="Endpoint Denial of Service"
                description="Adversaries may perform endpoint denial of service (DoS) attacks to degrade or block the availability of services."
              />
            </div>

            <ThreatXAIExplanation 
              attackType={selectedAlert.attack_type}
              contributions={mockShapData}
            />
          </div>
        )}
      </SheetContent>
    </Sheet>
  );
};
