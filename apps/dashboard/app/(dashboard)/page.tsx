export default function Page() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold tracking-tight">Live Incident Feed</h2>
          <p className="text-muted-foreground mt-1">Real-time threat detection from the XGBoost Champion model.</p>
        </div>
        <div className="flex gap-2">
          <button className="px-4 py-2 bg-background border border-border rounded-md text-sm font-medium hover:bg-accent transition-colors">Pause Feed</button>
          <button className="px-4 py-2 bg-primary text-primary-foreground rounded-md text-sm font-medium hover:bg-primary/90 transition-colors">Export Report</button>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        {[
          { title: "Critical Threats (24h)", value: "142", trend: "+12.5%", color: "text-severity-critical" },
          { title: "High Severity", value: "849", trend: "+4.1%", color: "text-severity-high" },
          { title: "Inference Latency", value: "42ms", trend: "-2ms", color: "text-emerald-500" },
          { title: "Active Ingestion", value: "14.2k/s", trend: "Stable", color: "text-muted-foreground" },
        ].map((kpi, i) => (
          <div key={i} className="bg-card border border-border rounded-xl p-5 shadow-sm">
            <h3 className="text-sm font-medium text-muted-foreground">{kpi.title}</h3>
            <div className="mt-2 flex items-baseline gap-2">
              <span className={`text-3xl font-bold tracking-tight ${kpi.color}`}>{kpi.value}</span>
              <span className="text-xs font-medium text-muted-foreground bg-accent px-2 py-0.5 rounded-full">{kpi.trend}</span>
            </div>
          </div>
        ))}
      </div>

      {/* Placeholder Table */}
      <div className="bg-card border border-border rounded-xl shadow-sm overflow-hidden flex flex-col">
        <div className="px-6 py-4 border-b border-border flex justify-between items-center bg-muted/30">
          <h3 className="font-semibold">Recent Predictions</h3>
          <div className="flex gap-2">
            <span className="px-2.5 py-1 rounded-md bg-severity-critical/10 text-severity-critical text-xs font-medium border border-severity-critical/20">DDoS</span>
            <span className="px-2.5 py-1 rounded-md bg-severity-high/10 text-severity-high text-xs font-medium border border-severity-high/20">BruteForce</span>
          </div>
        </div>
        <div className="p-12 flex flex-col items-center justify-center text-center">
          <div className="w-16 h-16 rounded-full bg-accent flex items-center justify-center mb-4 text-muted-foreground">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
          </div>
          <h4 className="text-lg font-medium text-foreground">Waiting for API Integration</h4>
          <p className="text-muted-foreground max-w-sm mt-2">
            The data ingestion pipeline (Phase 9) has not been built yet. 
            Security events will stream into this table in real-time once the backend is connected.
          </p>
        </div>
      </div>
    </div>
  );
}
