import React from "react";
import { cn } from "../lib/utils";

export type Severity = "CRITICAL" | "HIGH" | "MEDIUM" | "LOW";

const SeverityColors: Record<Severity, string> = {
  CRITICAL: "border-severity-critical text-severity-critical bg-severity-critical/10",
  HIGH: "border-severity-high text-severity-high bg-severity-high/10",
  MEDIUM: "border-severity-medium text-severity-medium bg-severity-medium/10",
  LOW: "border-severity-low text-severity-low bg-severity-low/10",
};

export const SeverityBadge = ({ severity, className }: { severity: Severity | string; className?: string }) => {
  const colorClass = SeverityColors[severity as Severity] || SeverityColors.LOW;
  return (
    <span className={cn("px-2 py-0.5 text-[10px] font-bold tracking-wider rounded-sm border", colorClass, className)}>
      {severity}
    </span>
  );
};
