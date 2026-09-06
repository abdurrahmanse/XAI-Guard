import { AlertTriangle, Activity, ShieldAlert, Terminal } from "lucide-react";

export default function DashboardHome() {
  return (
    <div className="min-h-screen bg-slate-50 font-sans">
      <div className="max-w-7xl mx-auto px-6 py-12">
        <header className="mb-10">
          <h1 className="text-3xl font-bold text-slate-900 flex items-center gap-3">
            <ShieldAlert className="w-8 h-8 text-rose-500" />
            SOC Analyst Dashboard
          </h1>
          <p className="text-slate-500 mt-2">Real-time threat monitoring and XAI explanations.</p>
        </header>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">
          <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-sm font-semibold text-slate-500 uppercase tracking-wider">Active Alerts</h3>
              <AlertTriangle className="w-5 h-5 text-amber-500" />
            </div>
            <p className="text-4xl font-bold text-slate-900">12</p>
            <p className="text-sm text-rose-500 font-medium mt-2">+3 since last hour</p>
          </div>
          
          <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-sm font-semibold text-slate-500 uppercase tracking-wider">Model Confidence</h3>
              <Activity className="w-5 h-5 text-emerald-500" />
            </div>
            <p className="text-4xl font-bold text-slate-900">98.2%</p>
            <p className="text-sm text-emerald-500 font-medium mt-2">Champion Model: XGBoost</p>
          </div>

          <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-sm font-semibold text-slate-500 uppercase tracking-wider">Events Analyzed</h3>
              <Terminal className="w-5 h-5 text-blue-500" />
            </div>
            <p className="text-4xl font-bold text-slate-900">1.4M</p>
            <p className="text-sm text-slate-500 font-medium mt-2">Past 24 hours</p>
          </div>
        </div>

        <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-8 text-center">
          <p className="text-slate-500">Live event stream will appear here...</p>
        </div>
      </div>
    </div>
  );
}
