import React from "react";
import { Check, Plus } from "lucide-react";

export default function PricingPage() {
  return (
    <div className="flex-1 py-24 max-w-7xl mx-auto px-6 w-full">
      <div className="text-center mb-16">
        <h1 className="text-4xl sm:text-6xl font-bold tracking-tight mb-4">Simple, transparent pricing</h1>
        <p className="text-xl text-muted-foreground max-w-2xl mx-auto">No hidden fees. Just powerful threat detection for teams of all sizes.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-24">
        {[
          { name: "Starter", price: "$499", features: ["1M Events / month", "Basic XAI Explanations", "Community Support", "Data Retention: 7 Days"] },
          { name: "Enterprise", price: "$1,999", features: ["100M Events / month", "Full SHAP/LIME Integration", "MITRE ATT&CK Mapping", "24/7 Phone Support", "Data Retention: 90 Days"], popular: true },
          { name: "Custom", price: "Contact Us", features: ["Unlimited Events", "Custom ML Models", "Dedicated Account Manager", "On-Premises Deployment", "Infinite Retention"] }
        ].map((plan, i) => (
          <div key={i} className={`p-8 rounded-3xl border flex flex-col gap-6 ${plan.popular ? 'border-primary shadow-lg relative bg-primary/5' : 'border-border/50 bg-card'}`}>
            {plan.popular && <div className="absolute -top-4 left-1/2 -translate-x-1/2 bg-primary text-primary-foreground text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider">Most Popular</div>}
            <div>
              <h3 className="text-2xl font-bold">{plan.name}</h3>
              <div className="mt-4 flex items-baseline text-5xl font-extrabold">
                {plan.price}
                {plan.price !== "Contact Us" && <span className="ml-1 text-xl font-medium text-muted-foreground">/mo</span>}
              </div>
            </div>
            <ul className="mt-6 space-y-4 flex-1">
              {plan.features.map(f => (
                <li key={f} className="flex gap-3">
                  <Check className="w-5 h-5 text-primary shrink-0" />
                  <span className="text-muted-foreground">{f}</span>
                </li>
              ))}
            </ul>
            <a href={plan.popular ? "/signup" : "/contact"} className={`w-full flex justify-center py-3 px-4 rounded-xl text-sm font-medium transition-colors ${plan.popular ? 'bg-primary text-primary-foreground hover:bg-primary/90' : 'bg-secondary text-secondary-foreground hover:bg-secondary/80'}`}>
              Get Started
            </a>
          </div>
        ))}
      </div>

      {/* FAQ Section */}
      <div className="max-w-3xl mx-auto">
        <h2 className="text-3xl font-bold text-center mb-10">Frequently Asked Questions</h2>
        <div className="space-y-4">
          {[
            { q: "How is an 'Event' defined?", a: "An event is a single network request or log entry processed by our ML models. Background heartbeat pings are not counted against your quota." },
            { q: "Can we deploy XAI-Guard on-premises?", a: "Yes. Our Custom plan supports full air-gapped or on-premises deployments using Docker/Kubernetes." },
            { q: "Do you offer a free trial?", a: "We offer a 14-day full-feature trial of the Enterprise plan with no credit card required." },
            { q: "What happens if we exceed our event quota?", a: "We will never block your security monitoring. We'll simply alert your admin and gracefully bill for overages at the end of the month." },
          ].map((faq, i) => (
            <div key={i} className="border border-border/50 rounded-xl p-6 bg-card">
              <h4 className="font-bold text-lg mb-2 flex justify-between items-center">
                {faq.q}
              </h4>
              <p className="text-muted-foreground">{faq.a}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
