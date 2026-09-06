import Link from 'next/link';

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex h-screen bg-background text-foreground overflow-hidden">
      {/* Sidebar */}
      <aside className="w-64 border-r border-border bg-card flex flex-col shadow-lg z-10">
        <div className="h-16 flex items-center px-6 border-b border-border">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-severity-critical flex items-center justify-center">
              <span className="text-white font-bold tracking-tighter">XG</span>
            </div>
            <div>
              <h2 className="font-bold text-lg tracking-tight leading-tight">XAI-Guard</h2>
              <p className="text-[10px] text-muted-foreground uppercase tracking-widest">SOC Interface</p>
            </div>
          </div>
        </div>
        
        <nav className="flex-1 px-4 py-6 space-y-1 overflow-y-auto">
          <div className="text-xs font-semibold text-muted-foreground mb-4 uppercase tracking-wider px-2">Core Modules</div>
          <Link href="/" className="flex items-center gap-3 px-3 py-2.5 rounded-md bg-accent text-accent-foreground text-sm font-medium transition-colors">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>
            Live Feed
          </Link>
          <Link href="/alerts" className="flex items-center gap-3 px-3 py-2.5 rounded-md hover:bg-accent/50 text-muted-foreground hover:text-foreground text-sm font-medium transition-colors">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><path d="M12 9v4"/><path d="M12 17h.01"/></svg>
            Alert Registry
          </Link>
          <Link href="/metrics" className="flex items-center gap-3 px-3 py-2.5 rounded-md hover:bg-accent/50 text-muted-foreground hover:text-foreground text-sm font-medium transition-colors">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M3 3v18h18"/><path d="m19 9-5 5-4-4-3 3"/></svg>
            System Metrics
          </Link>
          <Link href="/models" className="flex items-center gap-3 px-3 py-2.5 rounded-md hover:bg-accent/50 text-muted-foreground hover:text-foreground text-sm font-medium transition-colors">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="m21 16-9 5-9-5"/><path d="m21 8-9 5-9-5"/><path d="m12 15 9-5-9-5-9 5 9 5Z"/></svg>
            Model Hub
          </Link>
        </nav>
        
        <div className="p-4 border-t border-border">
          <div className="flex items-center gap-3">
            <div className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></div>
            <span className="text-xs font-medium text-muted-foreground">API Connected</span>
          </div>
        </div>
      </aside>

      {/* Main Content area */}
      <div className="flex-1 flex flex-col h-screen overflow-hidden">
        {/* Top Header */}
        <header className="h-16 border-b border-border bg-background flex items-center justify-between px-8 shrink-0">
          <h1 className="text-xl font-semibold">Security Operations Center</h1>
          <div className="flex items-center gap-4 text-sm">
            <span className="text-muted-foreground">Analyst ID: <span className="text-foreground font-mono">SOC-9482</span></span>
            <div className="w-8 h-8 rounded-full bg-accent flex items-center justify-center border border-border">
              <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
            </div>
          </div>
        </header>

        {/* Scrollable Content */}
        <main className="flex-1 overflow-auto bg-muted/20 p-8">
          <div className="max-w-7xl mx-auto">
            {children}
          </div>
        </main>
      </div>
    </div>
  );
}
