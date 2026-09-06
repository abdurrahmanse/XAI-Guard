import Link from 'next/link';
import { ThemeToggle } from '@/components/ThemeToggle';

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen bg-background text-foreground selection:bg-primary selection:text-primary-foreground">
      {/* Floating Modern Header */}
      <div className="fixed top-0 w-full flex justify-center pt-6 z-50 pointer-events-none">
        <header className="pointer-events-auto flex items-center justify-between px-6 py-3 bg-background/70 backdrop-blur-xl border border-white/10 rounded-full shadow-2xl w-full max-w-5xl transition-all">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-severity-critical to-severity-high flex items-center justify-center shadow-lg shadow-severity-critical/20">
              <span className="text-white font-bold text-xs tracking-tighter">XG</span>
            </div>
            <h1 className="font-semibold tracking-tight">XAI-Guard</h1>
          </div>
          
          <nav className="hidden md:flex items-center gap-1 bg-white/5 p-1 rounded-full border border-white/5">
            <Link href="/" className="px-4 py-1.5 rounded-full bg-white/10 text-sm font-medium transition-all text-foreground shadow-sm">Overview</Link>
            <Link href="/alerts" className="px-4 py-1.5 rounded-full text-muted-foreground hover:text-foreground hover:bg-white/5 text-sm font-medium transition-all">Threats</Link>
            <Link href="/metrics" className="px-4 py-1.5 rounded-full text-muted-foreground hover:text-foreground hover:bg-white/5 text-sm font-medium transition-all">Network</Link>
            <Link href="/models" className="px-4 py-1.5 rounded-full text-muted-foreground hover:text-foreground hover:bg-white/5 text-sm font-medium transition-all">AI Models</Link>
          </nav>
          
          <div className="flex items-center gap-3">
            <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-emerald-500/10 border border-emerald-500/20">
              <div className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></div>
              <span className="text-xs font-medium text-emerald-500">Live</span>
            </div>
            <div className="w-9 h-9 rounded-full bg-gradient-to-br from-muted to-muted/50 border border-black/10 dark:border-white/10"></div>
            <ThemeToggle />
          </div>
        </header>
      </div>

      {/* Main Content Area */}
      <main className="pt-32 pb-16 px-6 max-w-7xl mx-auto min-h-screen flex flex-col">
        {children}
      </main>
    </div>
  );
}
