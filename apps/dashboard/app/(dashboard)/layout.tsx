import { Shield, LayoutDashboard, Activity, AlertOctagon, Settings, LogOut, Bell, User } from "lucide-react";

import { MobileNav } from "../../components/mobile-nav";

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex h-screen overflow-hidden">
      {/* Sidebar */}
      <aside className="w-64 border-r bg-card hidden md:flex flex-col relative z-20 shadow-sm">
        <div className="h-16 flex items-center px-6 border-b">
          <Shield className="w-6 h-6 text-primary mr-3" />
          <span className="font-extrabold tracking-tight text-lg">XAI-Guard</span>
        </div>
        <div className="p-4">
          <div className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-2 px-3">Analytics</div>
          <nav className="space-y-1">
            <a href="/" className="flex items-center gap-3 px-3 py-2 rounded-lg text-sm bg-primary/10 text-primary font-medium">
              <LayoutDashboard className="w-4 h-4" /> Live Feed
            </a>
            <a href="/alerts" className="flex items-center gap-3 px-3 py-2 rounded-lg text-sm hover:bg-accent text-muted-foreground hover:text-foreground transition-colors">
              <AlertOctagon className="w-4 h-4" /> Threat History
            </a>
            <a href="/metrics" className="flex items-center gap-3 px-3 py-2 rounded-lg text-sm hover:bg-accent text-muted-foreground hover:text-foreground transition-colors">
              <Activity className="w-4 h-4" /> System Health
            </a>
          </nav>
        </div>
        <div className="mt-auto p-4">
          <nav className="space-y-1">
            <a href="/settings" className="flex items-center gap-3 px-3 py-2 rounded-lg text-sm hover:bg-accent text-muted-foreground hover:text-foreground transition-colors">
              <Settings className="w-4 h-4" /> Settings
            </a>
            <a href="/login" className="flex items-center gap-3 px-3 py-2 rounded-lg text-sm hover:bg-destructive/10 text-destructive hover:text-destructive transition-colors">
              <LogOut className="w-4 h-4" /> Logout
            </a>
          </nav>
        </div>
      </aside>

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col min-w-0 overflow-hidden relative">
        {/* Top Header */}
        <header className="h-16 border-b bg-card/50 backdrop-blur flex items-center justify-between px-6 z-10 sticky top-0">
          <div className="flex items-center">
            <MobileNav />
            <h2 className="text-sm font-medium text-muted-foreground">SOC Analyst Portal</h2>
          </div>
          <div className="flex items-center gap-4">
            <button className="relative p-2 text-muted-foreground hover:text-foreground transition-colors">
              <Bell className="w-5 h-5" />
              <span className="absolute top-1.5 right-1.5 w-2 h-2 rounded-full bg-red-500 animate-pulse"></span>
            </button>
            <div className="h-6 w-px bg-border"></div>
            <div className="flex items-center gap-3 cursor-pointer">
              <div className="w-8 h-8 rounded-full bg-primary/20 flex items-center justify-center text-primary border border-primary/30">
                <User className="w-4 h-4" />
              </div>
              <div className="hidden sm:block">
                <p className="text-sm font-medium leading-none">Security Analyst</p>
                <p className="text-xs text-muted-foreground mt-0.5">Tier 2 SOC</p>
              </div>
            </div>
          </div>
        </header>

        {/* Main Content */}
        <main className="flex-1 overflow-y-auto">
          {children}
        </main>
      </div>
    </div>
  );
}
// Force HMR update
