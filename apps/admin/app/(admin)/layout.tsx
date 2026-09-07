import { Database, LineChart, Shield, LayoutDashboard, LogOut, Bell, Settings } from "lucide-react";

export default function AdminLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex h-screen overflow-hidden bg-background">
      {/* Sidebar */}
      <aside className="w-64 border-r bg-card/50 hidden md:flex flex-col relative z-20 shadow-sm">
        <div className="h-16 flex items-center px-6 border-b">
          <Shield className="w-5 h-5 text-primary mr-2" />
          <span className="font-bold tracking-tight">Admin Console</span>
        </div>
        <div className="p-4">
          <div className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-2 px-3">Management</div>
          <nav className="flex-1 space-y-1">
            <a href="/" className="flex items-center gap-3 px-3 py-2 rounded-md text-sm hover:bg-accent text-muted-foreground hover:text-foreground">
              <LayoutDashboard className="w-4 h-4" /> Overview
            </a>
            <a href="/models" className="flex items-center gap-3 px-3 py-2 rounded-md text-sm bg-primary/10 text-primary font-medium">
              <Database className="w-4 h-4" /> Model Registry
            </a>
            <a href="/metrics" className="flex items-center gap-3 px-3 py-2 rounded-md text-sm hover:bg-accent text-muted-foreground hover:text-foreground">
              <LineChart className="w-4 h-4" /> System Metrics
            </a>
          </nav>
        </div>
        <div className="mt-auto p-4">
          <nav className="space-y-1">
            <a href="/settings" className="flex items-center gap-3 px-3 py-2 rounded-md text-sm hover:bg-accent text-muted-foreground hover:text-foreground transition-colors">
              <Settings className="w-4 h-4" /> Config
            </a>
            <a href="/login" className="flex items-center gap-3 px-3 py-2 rounded-md text-sm hover:bg-destructive/10 text-destructive hover:text-destructive transition-colors">
              <LogOut className="w-4 h-4" /> Sign Out
            </a>
          </nav>
        </div>
      </aside>
      {/* Main Content */}
      <div className="flex-1 flex flex-col min-w-0 overflow-hidden relative">
        {/* Top Header */}
        <header className="h-16 border-b bg-card/50 backdrop-blur flex items-center justify-between px-6 z-10 sticky top-0">
          <div className="flex items-center">
            <h2 className="text-sm font-medium text-muted-foreground">MLOps & Administration</h2>
          </div>
          <div className="flex items-center gap-4">
            <button className="relative p-2 text-muted-foreground hover:text-foreground transition-colors">
              <Bell className="w-5 h-5" />
            </button>
            <div className="h-6 w-px bg-border"></div>
            <div className="flex items-center gap-3 cursor-pointer">
              <div className="w-8 h-8 rounded-lg bg-emerald-500/10 flex items-center justify-center text-emerald-500 border border-emerald-500/20">
                DS
              </div>
              <div className="hidden sm:block">
                <p className="text-sm font-medium leading-none">Dr. Alan Turing</p>
                <p className="text-xs text-muted-foreground mt-0.5">Principal Data Scientist</p>
              </div>
            </div>
          </div>
        </header>

        <main className="flex-1 overflow-y-auto">
          {children}
        </main>
      </div>
    </div>
  );
}
