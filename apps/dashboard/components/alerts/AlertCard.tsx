import React from "react";
import { motion } from "framer-motion";
import { formatDistanceToNow } from "date-fns";
import { SeverityBadge } from "@xaiguard/ui";

interface AlertCardProps {
  alert: any;
  isSelected: boolean;
  onClick: () => void;
}

export const AlertCard = ({ alert, isSelected, onClick }: AlertCardProps) => {
  return (
    <motion.div
      initial={{ opacity: 0, x: -20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ duration: 0.2 }}
      onClick={onClick}
      className={`
        h-full p-4 rounded-lg cursor-pointer flex flex-col justify-center border transition-colors
        ${isSelected ? "bg-accent border-primary/50" : "bg-card border-border hover:border-primary/30"}
      `}
    >
      <div className="flex justify-between items-start">
        <div className="flex gap-3 items-center">
          <SeverityBadge severity={alert.severity} />
          <span className="font-mono text-sm">{alert.source_ip}</span>
          <span className="text-muted-foreground text-xs mx-1">→</span>
          <span className="font-mono text-sm">{alert.destination_ip}</span>
        </div>
        <span className="text-xs text-muted-foreground font-mono">
          {formatDistanceToNow(new Date(alert.last_seen_at), { addSuffix: true })}
        </span>
      </div>
      <div className="mt-2 flex justify-between items-end">
        <span className="text-sm font-medium">{alert.attack_type.replace(/_/g, " ")}</span>
        <div className="flex gap-2 text-xs">
          <span className="text-muted-foreground">Confidence:</span>
          <span className="font-medium">{(alert.confidence * 100).toFixed(1)}%</span>
        </div>
      </div>
    </motion.div>
  );
};
