"use client";

import React, { useRef, useEffect } from "react";
import { useVirtualizer } from "@tanstack/react-virtual";
import { useAlertsStore } from "@/stores/alerts-store";
import { AlertCard } from "./AlertCard";

export const AlertsFeed = () => {
  const alerts = useAlertsStore((state) => state.alerts);
  const setSelectedAlert = useAlertsStore((state) => state.setSelectedAlert);
  const selectedAlert = useAlertsStore((state) => state.selectedAlert);
  
  const parentRef = useRef<HTMLDivElement>(null);

  const rowVirtualizer = useVirtualizer({
    count: alerts.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 80,
    overscan: 5,
  });

  useEffect(() => {
    if (alerts.length > 0 && parentRef.current) {
      if (parentRef.current.scrollTop < 100) {
        rowVirtualizer.scrollToIndex(0, { align: "start" });
      }
    }
  }, [alerts.length, rowVirtualizer]);

  if (alerts.length === 0) {
    return (
      <div className="flex h-full items-center justify-center text-muted-foreground p-8 text-center border rounded-xl border-dashed bg-card/20">
        <p>No active alerts. Waiting for telemetry...</p>
      </div>
    );
  }

  return (
    <div
      ref={parentRef}
      className="h-[calc(100vh-200px)] overflow-auto rounded-xl border bg-card/30"
      style={{ contain: "strict" }}
    >
      <div
        style={{
          height: `${rowVirtualizer.getTotalSize()}px`,
          width: "100%",
          position: "relative",
        }}
      >
        {rowVirtualizer.getVirtualItems().map((virtualRow) => {
          const alert = alerts[virtualRow.index];
          if (!alert) return null;
          
          return (
            <div
              key={alert.id}
              style={{
                position: "absolute",
                top: 0,
                left: 0,
                width: "100%",
                height: `${virtualRow.size}px`,
                transform: `translateY(${virtualRow.start}px)`,
              }}
              className="px-2 py-1"
            >
              <AlertCard 
                alert={alert}
                isSelected={selectedAlert?.id === alert.id}
                onClick={() => setSelectedAlert(alert)}
              />
            </div>
          );
        })}
      </div>
    </div>
  );
};
