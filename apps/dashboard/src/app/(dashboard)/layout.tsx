export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  // Real layout will include WebSocket context provider and server-component sidebar
  return (
    <div className="flex h-screen bg-background text-foreground">
      <aside className="w-64 border-r border-border">Sidebar</aside>
      <main className="flex-1 overflow-auto">{children}</main>
    </div>
  );
}
