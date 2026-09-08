"use client";

import React, { useState, useEffect } from "react";
import { Activity, ArrowRight, Zap, DollarSign, BrainCircuit, ShieldAlert } from "lucide-react";
import { ResponsiveContainer, ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, ZAxis } from "recharts";

const performanceData = [
  { name: "XGBoost-v2 (Champion)", latency: 12.5, f1: 0.965, size: 200, fill: "#3b82f6" },
  { name: "LightGBM-v3 (Challenger)", latency: 15.2, f1: 0.982, size: 200, fill: "#10b981" },
  { name: "IsolationForest-v1 (Anomaly)", latency: 8.4, f1: 0.890, size: 200, fill: "#8b5cf6" },
  { name: "Transformer-Net (Research)", latency: 85.0, f1: 0.991, size: 200, fill: "#f43f5e" },
];

export default function ModelsPage() {
  const [metrics, setMetrics] = useState<any>(null);

  useEffect(() => {
    // Mock fetching from API
    setTimeout(() => {
      setMetrics({
        champion_f1: 0.965,
        challenger_f1: 0.982,
        champion_latency_p99_ms: 12.5,
        challenger_latency_p99_ms: 15.2,
        discrepancy_rate: 0.03,
        traffic_scored: 1450000
      });
    }, 500);
  }, []);

  return (
    <div className="p-6 max-w-7xl mx-auto flex flex-col gap-8">
      <div>
        <h1 className="text-3xl font-bold tracking-tight text-foreground">Model Registry & Shadow Mode</h1>
        <p className="text-muted-foreground mt-2">Compare Champion vs Challenger models in real-time shadow inference.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="p-4 rounded-xl border border-border/50 bg-card shadow-sm flex flex-col gap-1">
          <span className="text-sm text-muted-foreground">Shadow Traffic Scored</span>
          <span className="text-2xl font-bold">{metrics ? metrics.traffic_scored.toLocaleString() : "..."}</span>
        </div>
        <div className="p-4 rounded-xl border border-border/50 bg-card shadow-sm flex flex-col gap-1">
          <span className="text-sm text-muted-foreground">Discrepancy Rate</span>
          <span className="text-2xl font-bold text-amber-500">{metrics ? (metrics.discrepancy_rate * 100).toFixed(1) + "%" : "..."}</span>
        </div>
        <div className="p-4 rounded-xl border border-border/50 bg-card shadow-sm flex flex-col gap-1">
          <span className="text-sm text-muted-foreground">Champion F1</span>
          <span className="text-2xl font-bold text-blue-500">{metrics ? metrics.champion_f1 : "..."}</span>
        </div>
        <div className="p-4 rounded-xl border border-border/50 bg-card shadow-sm flex flex-col gap-1">
          <span className="text-sm text-muted-foreground">Challenger F1</span>
          <span className="text-2xl font-bold text-emerald-500">{metrics ? metrics.challenger_f1 : "..."}</span>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 rounded-xl border border-border/50 bg-card shadow-sm p-6 flex flex-col gap-4">
          <h2 className="text-xl font-bold flex items-center gap-2">
            <Zap className="w-5 h-5 text-amber-500" />
            Performance vs Latency
          </h2>
          <div className="h-[400px] w-full">
            <ResponsiveContainer width="100%" height="100%">
              <ScatterChart margin={{ top: 20, right: 20, bottom: 20, left: 20 }}>
                <CartesianGrid strokeDasharray="3 3" opacity={0.2} />
                <XAxis type="number" dataKey="latency" name="Latency (ms)" unit="ms" />
                <YAxis type="number" dataKey="f1" name="F1 Score" domain={[0.85, 1.0]} />
                <ZAxis type="number" dataKey="size" range={[100, 400]} />
                <Tooltip cursor={{ strokeDasharray: '3 3' }} />
                <Scatter name="Models" data={performanceData} />
              </ScatterChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="rounded-xl border border-border/50 bg-card shadow-sm p-6 flex flex-col gap-4">
          <h2 className="text-xl font-bold flex items-center gap-2">
            <BrainCircuit className="w-5 h-5 text-purple-500" />
            Model Selection
          </h2>
          <p className="text-sm text-muted-foreground mb-4">
            The Challenger model has proven higher accuracy on shadow traffic. Promote to Champion?
          </p>

          <div className="flex flex-col gap-3 p-4 rounded-lg bg-blue-500/10 border border-blue-500/20">
            <div className="flex justify-between items-center">
              <span className="font-semibold text-blue-500">XGBoost-v2</span>
              <span className="text-xs bg-blue-500 text-white px-2 py-0.5 rounded-full">CHAMPION</span>
            </div>
            <div className="text-sm text-muted-foreground flex justify-between">
              <span>Latency: 12.5ms</span>
              <span>Cost: $1.2/M req</span>
            </div>
          </div>

          <div className="flex justify-center my-2">
            <ArrowRight className="w-5 h-5 text-muted-foreground rotate-90" />
          </div>

          <div className="flex flex-col gap-3 p-4 rounded-lg bg-emerald-500/10 border border-emerald-500/20">
            <div className="flex justify-between items-center">
              <span className="font-semibold text-emerald-500">LightGBM-v3</span>
              <span className="text-xs bg-emerald-500 text-white px-2 py-0.5 rounded-full">CHALLENGER</span>
            </div>
            <div className="text-sm text-muted-foreground flex justify-between">
              <span>Latency: 15.2ms</span>
              <span>Cost: $0.8/M req</span>
            </div>
          </div>

          <button className="mt-6 w-full py-2 bg-primary text-primary-foreground rounded-md font-semibold hover:bg-primary/90 transition-colors">
            Promote to Champion
          </button>
        </div>
      </div>
    </div>
  );
}
