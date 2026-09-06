import Link from 'next/link';

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex h-screen bg-background text-foreground">
      <aside className="w-64 border-r border-border bg-card flex flex-col">
        <div className="p-4 border-b border-border">
          <h2 className="font-bold text-xl tracking-tight">XAI-Guard</h2>
          <p className="text-xs text-muted-foreground">SOC Dashboard</p>
        </div>
        <nav className="flex-1 p-4 space-y-2">
          <Link href="/" className="block px-3 py-2 rounded-md hover:bg-accent text-sm font-medium">Live Feed</Link>
          <Link href="/alerts" className="block px-3 py-2 rounded-md hover:bg-accent text-sm font-medium">Alerts</Link>
          <Link href="/metrics" className="block px-3 py-2 rounded-md hover:bg-accent text-sm font-medium">Metrics</Link>
          <Link href="/models" className="block px-3 py-2 rounded-md hover:bg-accent text-sm font-medium">Models</Link>
        </nav>
      </aside>
      <main className="flex-1 overflow-auto bg-background">
        {children}
      </main>
    </div>
  );
}
