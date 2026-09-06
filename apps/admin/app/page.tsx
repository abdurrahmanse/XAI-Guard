import { Settings, Users, Server, Database } from "lucide-react";

export default function AdminHome() {
  return (
    <div className="min-h-screen bg-slate-900 text-slate-100 font-sans">
      <div className="flex h-screen overflow-hidden">
        {/* Sidebar */}
        <aside className="w-64 bg-slate-950 border-r border-slate-800 p-6 flex flex-col gap-6">
          <div className="flex items-center gap-2 text-indigo-400 mb-4">
            <Settings className="w-6 h-6" />
            <span className="text-lg font-bold">Platform Admin</span>
          </div>
          
          <nav className="flex flex-col gap-2">
            <a href="#" className="flex items-center gap-3 px-4 py-3 bg-indigo-500/10 text-indigo-400 rounded-lg font-medium transition-colors">
              <Server className="w-5 h-5" /> Infrastructure
            </a>
            <a href="#" className="flex items-center gap-3 px-4 py-3 text-slate-400 hover:text-slate-200 hover:bg-slate-800/50 rounded-lg font-medium transition-colors">
              <Database className="w-5 h-5" /> Model Registry
            </a>
            <a href="#" className="flex items-center gap-3 px-4 py-3 text-slate-400 hover:text-slate-200 hover:bg-slate-800/50 rounded-lg font-medium transition-colors">
              <Users className="w-5 h-5" /> Access Control
            </a>
          </nav>
        </aside>

        {/* Main Content */}
        <main className="flex-1 overflow-y-auto p-10">
          <header className="mb-10">
            <h1 className="text-3xl font-bold text-white">Infrastructure Overview</h1>
            <p className="text-slate-400 mt-2">Manage backend services, databases, and model deployments.</p>
          </header>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="bg-slate-800 rounded-xl border border-slate-700 p-6">
              <h2 className="text-lg font-semibold text-white mb-4">Service Health</h2>
              <ul className="space-y-4">
                <li className="flex justify-between items-center">
                  <span className="text-slate-300">FastAPI Backend</span>
                  <span className="px-3 py-1 bg-emerald-500/20 text-emerald-400 rounded-full text-xs font-semibold">ONLINE</span>
                </li>
                <li className="flex justify-between items-center">
                  <span className="text-slate-300">PostgreSQL</span>
                  <span className="px-3 py-1 bg-emerald-500/20 text-emerald-400 rounded-full text-xs font-semibold">ONLINE</span>
                </li>
                <li className="flex justify-between items-center">
                  <span className="text-slate-300">Redis Cache</span>
                  <span className="px-3 py-1 bg-emerald-500/20 text-emerald-400 rounded-full text-xs font-semibold">ONLINE</span>
                </li>
              </ul>
            </div>
            
            <div className="bg-slate-800 rounded-xl border border-slate-700 p-6 flex items-center justify-center text-center">
              <div>
                <Database className="w-12 h-12 text-indigo-400 mx-auto mb-4 opacity-50" />
                <p className="text-slate-400">Detailed system metrics loading...</p>
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
