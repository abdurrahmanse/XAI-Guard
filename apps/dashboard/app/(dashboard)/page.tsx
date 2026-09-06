export default function Page() {
  return (
    <div className="flex flex-col gap-6 sm:gap-8 animate-in fade-in slide-in-from-bottom-4 duration-1000">
      
      {/* Hero Section - Responsive text sizing */}
      <div className="flex flex-col items-center text-center py-8 sm:py-12 lg:py-16">
        <h2 className="text-3xl sm:text-4xl md:text-5xl lg:text-6xl xl:text-7xl font-bold tracking-tighter bg-clip-text text-transparent bg-gradient-to-b from-foreground to-foreground/50 px-4">
          Network Pulse
        </h2>
        <p className="text-muted-foreground mt-3 sm:mt-4 max-w-xs sm:max-w-md lg:max-w-lg text-sm sm:text-base lg:text-lg px-4">
          Real-time threat landscape analysis powered by explainable transformer models.
        </p>
      </div>

      {/* Modern Bento Grid - 5 Device Breakpoints */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 2xl:grid-cols-5 gap-4 sm:gap-6">
        
        {/* Large Bento Item - Threat Activity */}
        <div className="col-span-1 sm:col-span-2 lg:col-span-2 xl:col-span-2 2xl:col-span-3 row-span-1 sm:row-span-2 rounded-[2rem] bg-card/40 border border-white/5 backdrop-blur-sm p-6 sm:p-8 shadow-2xl relative overflow-hidden group hover:bg-card/60 transition-all duration-500 min-h-[200px] sm:min-h-[300px]">
          <div className="absolute top-0 right-0 p-4 sm:p-8 opacity-20 group-hover:opacity-40 transition-opacity">
            <svg className="w-20 h-20 sm:w-[120px] sm:h-[120px] text-severity-critical" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>
          </div>
          <div className="relative z-10 h-full flex flex-col">
            <h3 className="text-lg sm:text-xl font-medium">Critical Activity</h3>
            <p className="text-muted-foreground mt-1 text-xs sm:text-sm">Last 24 hours</p>
            <div className="mt-auto pt-8 sm:pt-16 flex flex-wrap items-end gap-3 sm:gap-4">
              <span className="text-5xl sm:text-7xl font-bold tracking-tighter leading-none">142</span>
              <span className="text-severity-critical font-medium px-2 sm:px-3 py-1 rounded-full bg-severity-critical/10 border border-severity-critical/20 text-xs sm:text-sm mb-1 sm:mb-2">+12% surge</span>
            </div>
          </div>
        </div>

        {/* Small Bento Item 1 */}
        <div className="col-span-1 sm:col-span-1 lg:col-span-1 xl:col-span-1 2xl:col-span-1 rounded-[2rem] bg-card/40 border border-white/5 backdrop-blur-sm p-5 sm:p-6 shadow-xl flex flex-col gap-3 sm:gap-4 group hover:bg-card/60 transition-all duration-500">
          <div className="flex justify-between items-start">
            <div className="w-8 h-8 sm:w-10 sm:h-10 rounded-full bg-emerald-500/10 flex items-center justify-center text-emerald-500">
              <svg xmlns="http://www.w3.org/2000/svg" className="w-4 h-4 sm:w-5 sm:h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>
            </div>
            <span className="text-[10px] sm:text-xs font-medium text-emerald-500 bg-emerald-500/10 px-2 py-1 rounded-full border border-emerald-500/20">Optimum</span>
          </div>
          <div className="mt-auto pt-4">
            <p className="text-muted-foreground text-xs sm:text-sm line-clamp-1">Inference Latency</p>
            <h4 className="text-2xl sm:text-3xl lg:text-4xl font-semibold tracking-tight mt-1">42<span className="text-sm sm:text-lg text-muted-foreground ml-1">ms</span></h4>
          </div>
        </div>

        {/* Small Bento Item 2 */}
        <div className="col-span-1 sm:col-span-1 lg:col-span-3 xl:col-span-1 2xl:col-span-1 rounded-[2rem] bg-card/40 border border-white/5 backdrop-blur-sm p-5 sm:p-6 shadow-xl flex flex-col gap-3 sm:gap-4 group hover:bg-card/60 transition-all duration-500">
          <div className="flex justify-between items-start">
            <div className="w-8 h-8 sm:w-10 sm:h-10 rounded-full bg-blue-500/10 flex items-center justify-center text-blue-500">
              <svg xmlns="http://www.w3.org/2000/svg" className="w-4 h-4 sm:w-5 sm:h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
            </div>
            <span className="text-[10px] sm:text-xs font-medium text-blue-500 bg-blue-500/10 px-2 py-1 rounded-full border border-blue-500/20">Champion</span>
          </div>
          <div className="mt-auto pt-4">
            <p className="text-muted-foreground text-xs sm:text-sm line-clamp-1">Active Model</p>
            <h4 className="text-lg sm:text-xl lg:text-2xl font-semibold tracking-tight mt-1">XGBoost v2</h4>
          </div>
        </div>
        
      </div>

      {/* Glass Stream Table - Responsive layout */}
      <div className="mt-4 sm:mt-8 rounded-[2rem] bg-card/40 border border-white/5 backdrop-blur-md overflow-hidden shadow-2xl">
        <div className="px-4 sm:px-8 py-4 sm:py-6 border-b border-white/5 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 sm:gap-0 bg-white/[0.02]">
          <h3 className="font-medium text-base sm:text-lg">Incoming Threat Stream</h3>
          <button className="text-xs sm:text-sm px-4 py-2 rounded-full bg-white/5 hover:bg-white/10 transition-colors border border-white/5 w-full sm:w-auto">View All</button>
        </div>
        <div className="p-8 sm:p-16 flex flex-col items-center justify-center text-center min-h-[300px]">
          <div className="w-16 h-16 sm:w-20 sm:h-20 rounded-full bg-gradient-to-b from-white/10 to-white/5 flex items-center justify-center mb-4 sm:mb-6 shadow-inner border border-white/5">
            <svg xmlns="http://www.w3.org/2000/svg" className="w-8 h-8 sm:w-10 sm:h-10 text-muted-foreground/50" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" x2="12" y1="15" y2="3"/></svg>
          </div>
          <h4 className="text-lg sm:text-xl font-semibold bg-clip-text text-transparent bg-gradient-to-r from-foreground to-muted-foreground">Awaiting Ingestion</h4>
          <p className="text-muted-foreground mt-2 sm:mt-3 max-w-xs sm:max-w-md mx-auto text-xs sm:text-sm leading-relaxed">
            The Phase 9 data pipeline has not been activated. Connect the backend to stream live security events into this visualization.
          </p>
        </div>
      </div>

    </div>
  );
}
