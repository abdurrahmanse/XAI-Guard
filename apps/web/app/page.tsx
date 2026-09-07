import { Shield, ChevronRight, Activity, Network, Zap, Lock, BarChart3, Fingerprint, Eye } from "lucide-react";

export default function WebHome() {
  return (
    <div className="flex-1 w-full relative overflow-hidden">
      {/* Background gradients */}
      <div className="absolute top-0 left-0 w-full h-[600px] bg-gradient-to-b from-primary/5 via-primary/5 to-transparent pointer-events-none -z-10" />

      {/* Hero Section */}
      <section className="max-w-7xl mx-auto px-6 py-24 sm:py-32 flex flex-col items-center text-center">
        <div className="inline-flex items-center rounded-full border px-3 py-1 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 border-primary/20 bg-primary/10 text-primary hover:bg-primary/20 mb-8 gap-2">
          <Activity className="w-3.5 h-3.5" />
          XAI-Guard Enterprise Edition v1.0
        </div>
        
        <h1 className="text-5xl sm:text-7xl font-extrabold tracking-tight mb-8 text-foreground max-w-4xl">
          Explainable AI for <br className="hidden sm:block" />
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-500 to-emerald-500">
            Enterprise Threat Detection
          </span>
        </h1>
        
        <p className="text-muted-foreground text-xl max-w-2xl mb-12 leading-relaxed">
          The world's first multi-model threat detection platform that balances perfect classification accuracy with human-readable, actionable XAI explanations.
        </p>

        <div className="flex flex-col sm:flex-row gap-4 mb-24 w-full sm:w-auto">
          <a href="/login" className="inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 bg-primary text-primary-foreground hover:bg-primary/90 hover:scale-105 h-14 px-10 gap-2 shadow-lg w-full sm:w-auto text-lg">
            <Shield className="w-5 h-5" />
            Start Free Trial
          </a>
          <a href="/about" className="inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 border border-input bg-background hover:bg-accent hover:text-accent-foreground h-14 px-10 gap-2 shadow-sm hover:scale-105 w-full sm:w-auto text-lg">
            How it works
            <ChevronRight className="w-5 h-5" />
          </a>
        </div>
      </section>

      {/* Logos Section */}
      <section className="border-y border-border/40 bg-muted/20 py-12">
        <div className="max-w-7xl mx-auto px-6 text-center">
          <p className="text-sm font-semibold text-muted-foreground mb-8 uppercase tracking-widest">Trusted by Next-Generation Security Teams</p>
          <div className="flex flex-wrap justify-center items-center gap-12 sm:gap-24 opacity-50 grayscale">
            <h3 className="text-2xl font-black">AcmeCorp</h3>
            <h3 className="text-2xl font-black">GlobalBank</h3>
            <h3 className="text-2xl font-black">CyberTech</h3>
            <h3 className="text-2xl font-black">NexusSecurity</h3>
          </div>
        </div>
      </section>

      {/* Extensive Features Grid */}
      <section className="max-w-7xl mx-auto px-6 py-24 sm:py-32">
        <div className="text-center mb-20 max-w-3xl mx-auto">
          <h2 className="text-3xl sm:text-5xl font-bold tracking-tight mb-6">Everything you need to secure your perimeter.</h2>
          <p className="text-xl text-muted-foreground">Stop guessing why your ML models blocked traffic. XAI-Guard gives your SOC team complete transparency.</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          <div className="p-8 rounded-3xl bg-card border border-border/60 shadow-sm flex flex-col gap-5 hover:shadow-md transition-shadow">
            <div className="w-14 h-14 rounded-2xl bg-blue-500/10 flex items-center justify-center text-blue-500">
              <Network className="w-7 h-7" />
            </div>
            <h3 className="text-2xl font-bold">Real-time Ingestion</h3>
            <p className="text-muted-foreground leading-relaxed">Process millions of network events with Kafka-backed deduplication and lightning-fast Redis caching without breaking a sweat.</p>
          </div>
          
          <div className="p-8 rounded-3xl bg-card border border-border/60 shadow-sm flex flex-col gap-5 hover:shadow-md transition-shadow">
            <div className="w-14 h-14 rounded-2xl bg-emerald-500/10 flex items-center justify-center text-emerald-500">
              <Zap className="w-7 h-7" />
            </div>
            <h3 className="text-2xl font-bold">XAI Explanations</h3>
            <p className="text-muted-foreground leading-relaxed">Don't just flag threats. Understand them with integrated SHAP values and LIME feature contribution visualisations.</p>
          </div>
          
          <div className="p-8 rounded-3xl bg-card border border-border/60 shadow-sm flex flex-col gap-5 hover:shadow-md transition-shadow">
            <div className="w-14 h-14 rounded-2xl bg-rose-500/10 flex items-center justify-center text-rose-500">
               <Lock className="w-7 h-7" />
            </div>
            <h3 className="text-2xl font-bold">MITRE ATT&CK Mapping</h3>
            <p className="text-muted-foreground leading-relaxed">Every anomaly is automatically mapped to adversary tactics and techniques for immediate remediation and tracking.</p>
          </div>

          <div className="p-8 rounded-3xl bg-card border border-border/60 shadow-sm flex flex-col gap-5 hover:shadow-md transition-shadow">
            <div className="w-14 h-14 rounded-2xl bg-purple-500/10 flex items-center justify-center text-purple-500">
               <BarChart3 className="w-7 h-7" />
            </div>
            <h3 className="text-2xl font-bold">Champion / Challenger</h3>
            <p className="text-muted-foreground leading-relaxed">Continuous A/B testing of ML models in production. Automatically promote challengers when data drift occurs.</p>
          </div>

          <div className="p-8 rounded-3xl bg-card border border-border/60 shadow-sm flex flex-col gap-5 hover:shadow-md transition-shadow">
            <div className="w-14 h-14 rounded-2xl bg-amber-500/10 flex items-center justify-center text-amber-500">
               <Fingerprint className="w-7 h-7" />
            </div>
            <h3 className="text-2xl font-bold">Zero-Day Detection</h3>
            <p className="text-muted-foreground leading-relaxed">Identify anomalous patterns that rule-based systems miss using advanced Isolation Forests and XGBoost ensembles.</p>
          </div>

          <div className="p-8 rounded-3xl bg-card border border-border/60 shadow-sm flex flex-col gap-5 hover:shadow-md transition-shadow">
            <div className="w-14 h-14 rounded-2xl bg-cyan-500/10 flex items-center justify-center text-cyan-500">
               <Eye className="w-7 h-7" />
            </div>
            <h3 className="text-2xl font-bold">Full Observability</h3>
            <p className="text-muted-foreground leading-relaxed">Comprehensive dashboards for SOC analysts and data scientists. Know exactly what your system is doing at all times.</p>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-primary text-primary-foreground py-24 sm:py-32">
        <div className="max-w-4xl mx-auto px-6 text-center">
          <h2 className="text-4xl sm:text-5xl font-bold tracking-tight mb-6">Ready to secure your network?</h2>
          <p className="text-xl opacity-90 mb-10">Deploy XAI-Guard in your infrastructure in under 15 minutes.</p>
          <a href="/signup" className="inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium transition-colors bg-background text-foreground hover:bg-background/90 h-14 px-10 gap-2 shadow-lg text-lg">
            Create an Account
          </a>
        </div>
      </section>
    </div>
  );
}
// Force HMR update
