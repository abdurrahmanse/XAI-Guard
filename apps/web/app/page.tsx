import { Shield, Lock, Activity } from "lucide-react";

export default function WebHome() {
  return (
    <div className="min-h-screen bg-neutral-950 text-white font-sans selection:bg-emerald-500/30">
      <main className="max-w-6xl mx-auto px-6 py-32 flex flex-col items-center text-center">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 text-emerald-400 text-sm font-medium mb-8 border border-emerald-500/20">
          <Activity className="w-4 h-4" />
          <span>XAI-Guard Public Website</span>
        </div>
        
        <h1 className="text-5xl md:text-7xl font-bold tracking-tight mb-8">
          Explainable AI for <br className="hidden md:block" />
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 to-cyan-400">
            Cybersecurity Threat Detection
          </span>
        </h1>
        
        <p className="text-neutral-400 text-lg md:text-xl max-w-2xl mb-12 leading-relaxed">
          The world's first multi-model threat detection platform that balances perfect accuracy with human-readable explanations.
        </p>

        <div className="flex gap-4">
          <button className="bg-emerald-500 hover:bg-emerald-400 text-neutral-950 font-semibold px-8 py-3 rounded-lg transition-colors flex items-center gap-2">
            <Shield className="w-5 h-5" />
            Get Started
          </button>
          <button className="bg-neutral-800 hover:bg-neutral-700 text-white font-semibold px-8 py-3 rounded-lg transition-colors flex items-center gap-2 border border-neutral-700">
            <Lock className="w-5 h-5" />
            View Documentation
          </button>
        </div>
      </main>
    </div>
  );
}
