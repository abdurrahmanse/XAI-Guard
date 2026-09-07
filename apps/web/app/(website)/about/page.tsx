import React from "react";
import { Shield, Brain, Users, Globe } from "lucide-react";

export default function AboutPage() {
  return (
    <div className="flex-1 w-full">
      {/* Hero */}
      <section className="py-24 bg-muted/20 text-center px-6">
        <h1 className="text-4xl sm:text-6xl font-bold tracking-tight mb-8">Securing the Future, <br className="hidden sm:block"/> Transparently.</h1>
        <p className="text-xl text-muted-foreground max-w-2xl mx-auto leading-relaxed">
          XAI-Guard was founded by a team of security analysts and data scientists who were tired of black-box machine learning. We believe you should always know exactly <strong>why</strong> a threat was blocked.
        </p>
      </section>

      {/* Values */}
      <section className="py-24 max-w-7xl mx-auto px-6">
        <div className="text-center mb-16">
          <h2 className="text-3xl font-bold">Our Core Values</h2>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          <div className="p-6 rounded-2xl bg-card border shadow-sm text-center flex flex-col items-center">
            <div className="w-12 h-12 bg-primary/10 text-primary rounded-xl flex items-center justify-center mb-4"><Shield className="w-6 h-6"/></div>
            <h3 className="text-xl font-bold mb-2">Zero Trust</h3>
            <p className="text-muted-foreground text-sm">We verify every request mathematically and transparently.</p>
          </div>
          <div className="p-6 rounded-2xl bg-card border shadow-sm text-center flex flex-col items-center">
            <div className="w-12 h-12 bg-primary/10 text-primary rounded-xl flex items-center justify-center mb-4"><Brain className="w-6 h-6"/></div>
            <h3 className="text-xl font-bold mb-2">Explainable AI</h3>
            <p className="text-muted-foreground text-sm">Machine learning must be human-readable to be actionable.</p>
          </div>
          <div className="p-6 rounded-2xl bg-card border shadow-sm text-center flex flex-col items-center">
            <div className="w-12 h-12 bg-primary/10 text-primary rounded-xl flex items-center justify-center mb-4"><Users className="w-6 h-6"/></div>
            <h3 className="text-xl font-bold mb-2">For Analysts First</h3>
            <p className="text-muted-foreground text-sm">Our UI is designed to reduce alert fatigue for Tier 1 & 2 SOC teams.</p>
          </div>
          <div className="p-6 rounded-2xl bg-card border shadow-sm text-center flex flex-col items-center">
            <div className="w-12 h-12 bg-primary/10 text-primary rounded-xl flex items-center justify-center mb-4"><Globe className="w-6 h-6"/></div>
            <h3 className="text-xl font-bold mb-2">Global Scale</h3>
            <p className="text-muted-foreground text-sm">Processing billions of events seamlessly with Kafka and Redis.</p>
          </div>
        </div>
      </section>

      {/* Team Placeholder */}
      <section className="py-24 bg-card border-t px-6">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-3xl font-bold mb-6">Backed by the Best</h2>
          <p className="text-lg text-muted-foreground mb-12">
            Our platform is built by veterans from top cyber agencies and tech giants.
          </p>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            {[1, 2, 3, 4].map((i) => (
              <div key={i} className="flex flex-col items-center">
                <div className="w-24 h-24 rounded-full bg-muted border mb-4"></div>
                <h4 className="font-bold">Team Member {i}</h4>
                <p className="text-xs text-muted-foreground">Engineering</p>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}
