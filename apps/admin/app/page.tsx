import { Settings, Users, Server, Database, ChevronRight } from "lucide-react";

export default function AdminHome() {
  return (
    <div className="min-h-screen bg-background text-foreground font-sans flex overflow-hidden">
      
      {/* Shadcn Sidebar Pattern */}
      <aside className="w-64 border-r bg-muted/40 p-6 flex flex-col gap-6 h-screen">
        <div className="flex items-center gap-2 font-bold mb-4">
          <Settings className="w-5 h-5" />
          Platform Admin
        </div>
        
        <nav className="flex flex-col gap-1">
          <a href="#" className="flex items-center gap-3 px-3 py-2 bg-secondary text-secondary-foreground rounded-md text-sm font-medium transition-colors">
            <Server className="w-4 h-4" /> Infrastructure
          </a>
          <a href="#" className="flex items-center gap-3 px-3 py-2 text-muted-foreground hover:bg-muted hover:text-foreground rounded-md text-sm font-medium transition-colors">
            <Database className="w-4 h-4" /> Model Registry
          </a>
          <a href="#" className="flex items-center gap-3 px-3 py-2 text-muted-foreground hover:bg-muted hover:text-foreground rounded-md text-sm font-medium transition-colors">
            <Users className="w-4 h-4" /> Access Control
          </a>
        </nav>
      </aside>

      {/* Main Content */}
      <main className="flex-1 overflow-y-auto p-10 bg-background">
        <div className="max-w-5xl mx-auto space-y-8">
          
          <div className="flex items-center justify-between space-y-2">
            <div>
              <h2 className="text-3xl font-bold tracking-tight">Infrastructure Overview</h2>
              <p className="text-muted-foreground mt-1">Manage backend services, databases, and model deployments.</p>
            </div>
          </div>

          <div className="grid gap-6 md:grid-cols-2">
            
            {/* Shadcn Card: Service Health */}
            <div className="rounded-xl border bg-card text-card-foreground shadow-sm">
              <div className="flex flex-col space-y-1.5 p-6 pb-4">
                <h3 className="font-semibold leading-none tracking-tight">Service Health</h3>
                <p className="text-sm text-muted-foreground">Current status of backend dependencies.</p>
              </div>
              <div className="p-6 pt-0 space-y-4">
                
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className="w-2 h-2 rounded-full bg-emerald-500" />
                    <span className="text-sm font-medium">FastAPI Backend</span>
                  </div>
                  <span className="inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold text-emerald-500">Online</span>
                </div>

                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className="w-2 h-2 rounded-full bg-emerald-500" />
                    <span className="text-sm font-medium">PostgreSQL Database</span>
                  </div>
                  <span className="inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold text-emerald-500">Online</span>
                </div>

                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className="w-2 h-2 rounded-full bg-emerald-500" />
                    <span className="text-sm font-medium">Redis Cache</span>
                  </div>
                  <span className="inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold text-emerald-500">Online</span>
                </div>

              </div>
            </div>

            {/* Shadcn Card: Quick Actions */}
            <div className="rounded-xl border bg-card text-card-foreground shadow-sm">
              <div className="flex flex-col space-y-1.5 p-6 pb-4">
                <h3 className="font-semibold leading-none tracking-tight">Quick Actions</h3>
              </div>
              <div className="p-6 pt-0 flex flex-col gap-2">
                <button className="flex items-center justify-between w-full p-3 text-sm font-medium text-left border rounded-md hover:bg-muted transition-colors">
                  Trigger Model Evaluation Job
                  <ChevronRight className="w-4 h-4 text-muted-foreground" />
                </button>
                <button className="flex items-center justify-between w-full p-3 text-sm font-medium text-left border rounded-md hover:bg-muted transition-colors">
                  Purge Cache
                  <ChevronRight className="w-4 h-4 text-muted-foreground" />
                </button>
              </div>
            </div>

          </div>
        </div>
      </main>
    </div>
  );
}
