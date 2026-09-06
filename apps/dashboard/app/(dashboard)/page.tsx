export default function Page() {
  return (
    <div className="flex flex-col gap-8 animate-in fade-in slide-in-from-bottom-4 duration-1000">
      
      {/* Hero Section */}
      <div className="flex flex-col items-center text-center py-12">
        <h2 className="text-4xl md:text-6xl font-bold tracking-tighter bg-clip-text text-transparent bg-gradient-to-b from-foreground to-foreground/50">
          Network Pulse
        </h2>
        <p className="text-muted-foreground mt-4 max-w-lg text-lg">
          Real-time threat landscape analysis powered by explainable transformer models.
        </p>
      </div>

      {/* Modern Bento Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        
        {/* Large Bento Item - Threat Activity */}
        <div className="md:col-span-2 row-span-2 rounded-3xl bg-card/40 border border-white/5 backdrop-blur-sm p-8 shadow-2xl relative overflow-hidden group hover:bg-card/60 transition-all duration-500">
          <div className="absolute top-0 right-0 p-8 opacity-20 group-hover:opacity-40 transition-opacity">
            <svg width="120" height="120" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1" className="text-severity-critical"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>
          </div>
          <div className="relative z-10 h-full flex flex-col">
            <h3 className="text-xl font-medium">Critical Activity</h3>
            <p className="text-muted-foreground mt-1 text-sm">Last 24 hours</p>
            <div className="mt-auto pt-16">
              <span className="text-7xl font-bold tracking-tighter">142</span>
              <span className="text-severity-critical ml-4 font-medium px-3 py-1 rounded-full bg-severity-critical/10 border border-severity-critical/20">+12% surge</span>
            </div>
          </div>
        </div>

        {/* Small Bento Item 1 */}
        <div className="rounded-3xl bg-card/40 border border-white/5 backdrop-blur-sm p-6 shadow-xl flex flex-col gap-4 group hover:bg-card/60 transition-all duration-500">
          <div className="flex justify-between items-start">
            <div className="w-10 h-10 rounded-full bg-emerald-500/10 flex items-center justify-center text-emerald-500">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>
            </div>
            <span className="text-xs font-medium text-emerald-500 bg-emerald-500/10 px-2 py-1 rounded-full border border-emerald-500/20">Optimum</span>
          </div>
          <div>
            <p className="text-muted-foreground text-sm">Inference Latency</p>
            <h4 className="text-3xl font-semibold tracking-tight mt-1">42<span className="text-lg text-muted-foreground ml-1">ms</span></h4>
          </div>
        </div>

        {/* Small Bento Item 2 */}
        <div className="rounded-3xl bg-card/40 border border-white/5 backdrop-blur-sm p-6 shadow-xl flex flex-col gap-4 group hover:bg-card/60 transition-all duration-500">
          <div className="flex justify-between items-start">
            <div className="w-10 h-10 rounded-full bg-blue-500/10 flex items-center justify-center text-blue-500">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
            </div>
            <span className="text-xs font-medium text-blue-500 bg-blue-500/10 px-2 py-1 rounded-full border border-blue-500/20">Champion</span>
          </div>
          <div>
            <p className="text-muted-foreground text-sm">Active Model</p>
            <h4 className="text-xl font-semibold tracking-tight mt-1">XGBoost v2.1</h4>
          </div>
        </div>
        
      </div>

      {/* Glass Stream Table */}
      <div className="mt-8 rounded-3xl bg-card/40 border border-white/5 backdrop-blur-md overflow-hidden shadow-2xl">
        <div className="px-8 py-6 border-b border-white/5 flex justify-between items-center bg-white/[0.02]">
          <h3 className="font-medium text-lg">Incoming Threat Stream</h3>
          <button className="text-sm px-4 py-2 rounded-full bg-white/5 hover:bg-white/10 transition-colors border border-white/5">View All</button>
        </div>
        <div className="p-16 flex flex-col items-center justify-center text-center">
          <div className="w-20 h-20 rounded-full bg-gradient-to-b from-white/10 to-white/5 flex items-center justify-center mb-6 shadow-inner border border-white/5">
            <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" className="text-muted-foreground/50"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" x2="12" y1="15" y2="3"/></svg>
          </div>
          <h4 className="text-xl font-semibold bg-clip-text text-transparent bg-gradient-to-r from-foreground to-muted-foreground">Awaiting Ingestion</h4>
          <p className="text-muted-foreground mt-3 max-w-md mx-auto text-sm leading-relaxed">
            The Phase 9 data pipeline has not been activated. Connect the backend to stream live security events into this visualization.
          </p>
        </div>
      </div>

    </div>
  );
}
