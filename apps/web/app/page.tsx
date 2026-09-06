import { Shield, ChevronRight, Activity } from "lucide-react";

export default function WebHome() {
  return (
    <div className="min-h-screen bg-background text-foreground font-sans selection:bg-primary/30">
      <main className="max-w-5xl mx-auto px-6 py-32 flex flex-col items-center text-center">
        {/* Shadcn Badge Pattern */}
        <div className="inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 border-transparent bg-secondary text-secondary-foreground hover:bg-secondary/80 mb-8 gap-2">
          <Activity className="w-3.5 h-3.5" />
          XAI-Guard Platform v1.0
        </div>
        
        <h1 className="text-4xl sm:text-6xl font-extrabold tracking-tight mb-6 text-foreground">
          Explainable AI for <br className="hidden sm:block" />
          Cybersecurity Threat Detection
        </h1>
        
        <p className="text-muted-foreground text-lg sm:text-xl max-w-2xl mb-10 leading-relaxed">
          The world's first multi-model threat detection platform that balances perfect accuracy with human-readable, actionable explanations.
        </p>

        <div className="flex flex-col sm:flex-row gap-4">
          {/* Shadcn Primary Button */}
          <button className="inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 bg-primary text-primary-foreground hover:bg-primary/90 h-11 px-8 gap-2 shadow">
            <Shield className="w-4 h-4" />
            Get Started
          </button>
          {/* Shadcn Outline Button */}
          <button className="inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 border border-input bg-background hover:bg-accent hover:text-accent-foreground h-11 px-8 gap-2 shadow-sm">
            View Documentation
            <ChevronRight className="w-4 h-4" />
          </button>
        </div>
      </main>
    </div>
  );
}
