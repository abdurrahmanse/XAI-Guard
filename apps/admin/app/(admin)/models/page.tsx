"use client";

import React, { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { CheckCircle2, ArrowUpCircle, Clock, AlertTriangle, LineChart as LineChartIcon } from "lucide-react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";

const fetchRegistry = async () => {
  await new Promise(r => setTimeout(r, 800));
  return [
    { id: "xgb-v2.1", status: "CHAMPION", f1: 0.942, roc_auc: 0.981, p99_latency: 42, created_at: "2026-09-01T10:00:00Z" },
    { id: "xgb-v2.2-rc1", status: "CHALLENGER", f1: 0.958, roc_auc: 0.989, p99_latency: 45, created_at: "2026-09-05T14:30:00Z" },
    { id: "rf-v1.0", status: "ARCHIVED", f1: 0.891, roc_auc: 0.932, p99_latency: 85, created_at: "2026-08-15T09:00:00Z" },
  ];
};

const promoteModel = async (modelId: string) => {
  await new Promise(r => setTimeout(r, 500));
  return { success: true };
};

const mockDriftData = [
  { date: "09-01", f1: 0.950 },
  { date: "09-02", f1: 0.948 },
  { date: "09-03", f1: 0.945 },
  { date: "09-04", f1: 0.941 },
  { date: "09-05", f1: 0.938 },
  { date: "09-06", f1: 0.935 },
  { date: "09-07", f1: 0.932 },
];

export default function ModelsPage() {
  const queryClient = useQueryClient();
  const [promoting, setPromoting] = useState<string | null>(null);

  const { data: models, isLoading } = useQuery({
    queryKey: ["registry"],
    queryFn: fetchRegistry
  });

  const promoteMutation = useMutation({
    mutationFn: promoteModel,
    onSuccess: (_, variables) => {
      queryClient.setQueryData(["registry"], (old: any) => {
        if (!old) return old;
        return old.map((m: any) => ({
          ...m,
          status: m.id === variables ? "CHAMPION" : m.status === "CHAMPION" ? "ARCHIVED" : m.status
        }));
      });
      setPromoting(null);
    }
  });

  return (
    <div className="p-8 max-w-6xl mx-auto space-y-8">
      <div className="flex justify-between items-start">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Model Registry</h1>
          <p className="text-muted-foreground mt-2">Manage Champion/Challenger lifecycle and monitor drift.</p>
        </div>
        <button 
          onClick={async () => {
            try {
              const res = await fetch("http://localhost:8000/v1/training/trigger", { 
                method: "POST", 
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ force_repro: false }) 
              });
              if (res.ok) alert("Automated ML Pipeline Triggered via Celery! Check worker logs.");
              else alert("Failed to trigger pipeline");
            } catch (err) {
              alert("Network error: " + err);
            }
          }}
          className="inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors bg-blue-600 text-white shadow hover:bg-blue-700 h-10 px-6 gap-2"
        >
          Retrain Model
        </button>
      </div>

      <div className="bg-card border rounded-xl p-6 shadow-sm">
        <div className="flex items-center gap-2 mb-6">
          <LineChartIcon className="w-5 h-5 text-primary" />
          <h2 className="text-lg font-semibold">Active Champion F1 Drift (Last 7 Days)</h2>
        </div>
        <div className="h-64 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={mockDriftData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#333" vertical={false} />
              <XAxis dataKey="date" stroke="#888" fontSize={12} tickLine={false} axisLine={false} />
              <YAxis domain={[0.90, 0.96]} stroke="#888" fontSize={12} tickLine={false} axisLine={false} />
              <Tooltip 
                contentStyle={{ backgroundColor: '#111', borderColor: '#333', borderRadius: '8px' }}
                itemStyle={{ color: '#fff' }}
              />
              <Line 
                type="monotone" 
                dataKey="f1" 
                stroke="hsl(var(--primary))" 
                strokeWidth={3}
                dot={{ r: 4, fill: "hsl(var(--primary))" }}
                activeDot={{ r: 6 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
        <div className="mt-4 flex items-center gap-2 text-sm text-amber-500 bg-amber-500/10 p-3 rounded-lg border border-amber-500/20">
          <AlertTriangle className="w-4 h-4" />
          <span>Warning: Champion model <strong>xgb-v2.1</strong> has drifted below the 0.940 F1 threshold. Promotion of a Challenger is recommended.</span>
        </div>
      </div>

      <div className="bg-card border rounded-xl shadow-sm overflow-hidden">
        <table className="w-full text-sm text-left">
          <thead className="bg-muted/50 text-muted-foreground uppercase text-xs border-b">
            <tr>
              <th className="px-6 py-4 font-medium">Model ID</th>
              <th className="px-6 py-4 font-medium">Status</th>
              <th className="px-6 py-4 font-medium">F1 Score</th>
              <th className="px-6 py-4 font-medium">ROC-AUC</th>
              <th className="px-6 py-4 font-medium">p99 Latency</th>
              <th className="px-6 py-4 font-medium text-right">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y">
            {isLoading ? (
              <tr>
                <td colSpan={6} className="px-6 py-8 text-center text-muted-foreground">Loading registry...</td>
              </tr>
            ) : models?.map((model) => (
              <tr key={model.id} className="hover:bg-muted/30 transition-colors">
                <td className="px-6 py-4 font-mono font-medium">{model.id}</td>
                <td className="px-6 py-4">
                  {model.status === "CHAMPION" && <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold bg-emerald-500/15 text-emerald-500 border border-emerald-500/20"><CheckCircle2 className="w-3.5 h-3.5"/> Champion</span>}
                  {model.status === "CHALLENGER" && <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold bg-blue-500/15 text-blue-500 border border-blue-500/20"><ArrowUpCircle className="w-3.5 h-3.5"/> Challenger</span>}
                  {model.status === "ARCHIVED" && <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold bg-zinc-500/15 text-zinc-400 border border-zinc-500/20"><Clock className="w-3.5 h-3.5"/> Archived</span>}
                </td>
                <td className="px-6 py-4 font-mono">{model.f1.toFixed(3)}</td>
                <td className="px-6 py-4 font-mono">{model.roc_auc.toFixed(3)}</td>
                <td className="px-6 py-4 font-mono">{model.p99_latency}ms</td>
                <td className="px-6 py-4 text-right">
                  {model.status === "CHALLENGER" && (
                    <button 
                      onClick={() => {
                        setPromoting(model.id);
                        promoteMutation.mutate(model.id);
                      }}
                      disabled={promoting === model.id}
                      className="inline-flex items-center justify-center rounded-md text-xs font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:opacity-50 bg-primary text-primary-foreground shadow hover:bg-primary/90 h-8 px-4"
                    >
                      {promoting === model.id ? "Promoting..." : "Promote to Champion"}
                    </button>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
