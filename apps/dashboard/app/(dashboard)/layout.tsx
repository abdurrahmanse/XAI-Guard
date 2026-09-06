import Link from 'next/link';
import { ThemeToggle } from '@/components/ThemeToggle';

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen bg-background text-foreground selection:bg-primary selection:text-primary-foreground">
      {/* Floating Modern Header - Responsive */}
      <div className="fixed top-0 w-full flex justify-center pt-4 sm:pt-6 z-50 pointer-events-none px-4 sm:px-6">
        <header className="pointer-events-auto flex items-center justify-between px-4 sm:px-6 py-3 bg-background/70 backdrop-blur-xl border border-white/10 rounded-full shadow-2xl w-full max-w-[1920px] 2xl:max-w-7xl xl:max-w-5xl lg:max-w-4xl transition-all">
          <div className="flex items-center gap-2 sm:gap-3">
            <div className="w-7 h-7 sm:w-8 sm:h-8 rounded-full bg-gradient-to-tr from-severity-critical to-severity-high flex items-center justify-center shadow-lg shadow-severity-critical/20">
              <span className="text-white font-bold text-[10px] sm:text-xs tracking-tighter">XG</span>
            </div>
            <h1 className="font-semibold tracking-tight text-sm sm:text-base hidden sm:block">XAI-Guard</h1>
          </div>
          
          {/* Navigation - Hidden on mobile/sm, visible md and up */}
          <nav className="hidden md:flex items-center gap-1 bg-white/5 p-1 rounded-full border border-white/5">
            <Link href="/" className="px-3 lg:px-4 py-1.5 rounded-full bg-white/10 text-xs lg:text-sm font-medium transition-all text-foreground shadow-sm">Overview</Link>
            <Link href="/alerts" className="px-3 lg:px-4 py-1.5 rounded-full text-muted-foreground hover:text-foreground hover:bg-white/5 text-xs lg:text-sm font-medium transition-all">Threats</Link>
            <Link href="/metrics" className="px-3 lg:px-4 py-1.5 rounded-full text-muted-foreground hover:text-foreground hover:bg-white/5 text-xs lg:text-sm font-medium transition-all">Network</Link>
            <Link href="/models" className="px-3 lg:px-4 py-1.5 rounded-full text-muted-foreground hover:text-foreground hover:bg-white/5 text-xs lg:text-sm font-medium transition-all">AI Models</Link>
          </nav>
          
          <div className="flex items-center gap-2 sm:gap-3">
            <div className="flex items-center gap-1.5 sm:gap-2 px-2 sm:px-3 py-1 sm:py-1.5 rounded-full bg-emerald-500/10 border border-emerald-500/20">
              <div className="w-1.5 h-1.5 sm:w-2 sm:h-2 rounded-full bg-emerald-500 animate-pulse"></div>
              <span className="text-[10px] sm:text-xs font-medium text-emerald-500">Live</span>
            </div>
            <div className="w-7 h-7 sm:w-9 sm:h-9 rounded-full bg-gradient-to-br from-muted to-muted/50 border border-black/10 dark:border-white/10 flex items-center justify-center">
              <span className="text-[10px] sm:text-xs text-muted-foreground hidden sm:block">A</span>
            </div>
            <ThemeToggle />
            {/* Mobile Menu Icon */}
            <button className="md:hidden w-8 h-8 flex flex-col justify-center items-center gap-1 bg-white/5 rounded-full">
              <span className="w-3 h-[2px] bg-foreground rounded-full"></span>
              <span className="w-4 h-[2px] bg-foreground rounded-full"></span>
              <span className="w-3 h-[2px] bg-foreground rounded-full"></span>
            </button>
          </div>
        </header>
      </div>

      {/* Main Content Area - Responsive padding */}
      <main className="pt-24 sm:pt-32 pb-16 px-4 sm:px-6 lg:px-8 max-w-[1920px] 2xl:max-w-7xl mx-auto min-h-screen flex flex-col">
        {children}
      </main>
    </div>
  );
}
