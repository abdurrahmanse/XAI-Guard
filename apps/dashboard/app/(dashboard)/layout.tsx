import { ReactNode } from "react";
import { cookies } from "next/headers";
import Link from "next/link";
import { Shield, LayoutDashboard, Activity, Server, LogOut } from "lucide-react";
import { ThemeToggle } from '@/components/ThemeToggle';

export default async function DashboardLayout({ children }: { children: ReactNode }) {
  const cookieStore = await cookies();
  const token = cookieStore.get("access_token")?.value;
  
  let user = { username: "Unknown", role: "guest" };
  if (token) {
    try {
      const payload = JSON.parse(atob(token.split(".")[1] || ""));
      user = { username: payload.sub, role: payload.role || "analyst" };
    } catch (e) {
      // ignore
    }
  }

  return (
    <div className="flex h-screen bg-background text-foreground overflow-hidden">
      {/* Sidebar */}
      <aside className="w-64 border-r border-border bg-card flex flex-col justify-between hidden md:flex z-10">
        <div>
          <div className="flex h-16 items-center justify-between border-b border-border px-6">
            <div className="flex items-center">
              <Shield className="mr-2 h-6 w-6 text-primary" />
              <span className="text-lg font-bold tracking-tight">XAI-Guard</span>
            </div>
            <ThemeToggle />
          </div>
          <nav className="space-y-1 p-4">
            <Link href="/" className="flex items-center rounded-md px-3 py-2 text-sm font-medium text-foreground hover:bg-accent hover:text-accent-foreground transition-colors">
              <LayoutDashboard className="mr-3 h-5 w-5 text-muted-foreground" />
              Live Alerts
            </Link>
            <Link href="/metrics" className="flex items-center rounded-md px-3 py-2 text-sm font-medium text-foreground hover:bg-accent hover:text-accent-foreground transition-colors">
              <Activity className="mr-3 h-5 w-5 text-muted-foreground" />
              Metrics
            </Link>
            <Link href="/models" className="flex items-center rounded-md px-3 py-2 text-sm font-medium text-foreground hover:bg-accent hover:text-accent-foreground transition-colors">
              <Server className="mr-3 h-5 w-5 text-muted-foreground" />
              Model Registry
            </Link>
          </nav>
        </div>
        
        <div className="border-t border-border p-4">
          <div className="mb-4 px-3">
            <p className="text-sm font-medium">{user.username}</p>
            <p className="text-xs text-muted-foreground capitalize">{user.role}</p>
          </div>
          <form action="/logout" method="POST">
            <button type="submit" className="flex w-full items-center rounded-md px-3 py-2 text-sm font-medium text-destructive hover:bg-destructive/10 transition-colors">
              <LogOut className="mr-3 h-5 w-5" />
              Sign out
            </button>
          </form>
        </div>
      </aside>
      
      {/* Main Content */}
      <main className="flex-1 overflow-y-auto relative">
        <div className="md:hidden flex h-16 items-center justify-between border-b border-border px-6 bg-card">
          <div className="flex items-center">
            <Shield className="mr-2 h-6 w-6 text-primary" />
            <span className="text-lg font-bold tracking-tight">XAI-Guard</span>
          </div>
          <ThemeToggle />
        </div>
        <div className="p-6">
          {children}
        </div>
      </main>
    </div>
  );
}
