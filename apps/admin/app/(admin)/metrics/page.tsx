import React from "react";
import { Activity, Cpu, HardDrive, Network, ServerCrash, Users } from "lucide-react";

export default function MetricsPage() {
  return (
    <div className="p-8 max-w-6xl mx-auto space-y-8">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">System Metrics</h1>
        <p className="text-muted-foreground mt-2">Real-time observability for ML inference and backend infrastructure.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {/* Metric Card 1 */}
        <div className="bg-card border rounded-xl p-6 shadow-sm flex flex-col gap-4">
          <div className="flex justify-between items-start">
            <div className="p-2 bg-emerald-500/10 text-emerald-500 rounded-lg">
              <Activity className="w-5 h-5" />
            </div>
            <span className="text-xs font-bold text-emerald-500 bg-emerald-500/10 px-2 py-1 rounded-full border border-emerald-500/20">HEALTHY</span>
          </div>
          <div>
            <p className="text-muted-foreground text-sm">Global Inference Latency</p>
            <h3 className="text-3xl font-bold mt-1">42<span className="text-xl text-muted-foreground ml-1">ms</span></h3>
            <p className="text-xs text-muted-foreground mt-2 font-mono">p99: 85ms | p50: 38ms</p>
          </div>
        </div>

        {/* Metric Card 2 */}
        <div className="bg-card border rounded-xl p-6 shadow-sm flex flex-col gap-4">
          <div className="flex justify-between items-start">
            <div className="p-2 bg-blue-500/10 text-blue-500 rounded-lg">
              <Network className="w-5 h-5" />
            </div>
            <span className="text-xs font-bold text-blue-500 bg-blue-500/10 px-2 py-1 rounded-full border border-blue-500/20">STABLE</span>
          </div>
          <div>
            <p className="text-muted-foreground text-sm">Event Ingestion Rate</p>
            <h3 className="text-3xl font-bold mt-1">1,245<span className="text-xl text-muted-foreground ml-1">/sec</span></h3>
            <p className="text-xs text-muted-foreground mt-2 font-mono">Kafka Offset Lag: 0</p>
          </div>
        </div>

        {/* Metric Card 3 */}
        <div className="bg-card border rounded-xl p-6 shadow-sm flex flex-col gap-4">
          <div className="flex justify-between items-start">
            <div className="p-2 bg-purple-500/10 text-purple-500 rounded-lg">
              <Users className="w-5 h-5" />
            </div>
          </div>
          <div>
            <p className="text-muted-foreground text-sm">Active SOC Analysts</p>
            <h3 className="text-3xl font-bold mt-1">24</h3>
            <p className="text-xs text-muted-foreground mt-2 font-mono">WebSocket Conns: 48</p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-card border rounded-xl p-6 shadow-sm">
          <div className="flex items-center gap-2 mb-6">
            <Cpu className="w-5 h-5 text-primary" />
            <h2 className="text-lg font-semibold">Model Server CPU Load</h2>
          </div>
          <div className="h-4 w-full bg-secondary rounded-full overflow-hidden mb-2">
            <div className="h-full bg-primary" style={{ width: '65%' }}></div>
          </div>
          <p className="text-right text-xs font-mono text-muted-foreground">65% (Auto-scaling at 80%)</p>
        </div>

        <div className="bg-card border rounded-xl p-6 shadow-sm">
          <div className="flex items-center gap-2 mb-6">
            <HardDrive className="w-5 h-5 text-primary" />
            <h2 className="text-lg font-semibold">Redis Cache Memory</h2>
          </div>
          <div className="h-4 w-full bg-secondary rounded-full overflow-hidden mb-2">
            <div className="h-full bg-blue-500" style={{ width: '42%' }}></div>
          </div>
          <p className="text-right text-xs font-mono text-muted-foreground">3.2 GB / 8.0 GB (42%)</p>
        </div>
      </div>
    </div>
  );
}
