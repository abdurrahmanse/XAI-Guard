export default function AdminLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex flex-col min-h-screen bg-background text-foreground">
      <header className="h-16 border-b border-border">Admin Topbar</header>
      <main className="flex-1 container mx-auto py-6">{children}</main>
    </div>
  );
}
