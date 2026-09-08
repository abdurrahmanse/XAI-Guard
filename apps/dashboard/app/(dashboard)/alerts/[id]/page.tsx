"use client";

import React, { useState, useEffect } from "react";
import { AlertTriangle, Fingerprint, Shield, Cpu, Activity, Clock, Network, Zap } from "lucide-react";
import { FeatureContributionBar, MitreBadge, SeverityBadge } from "@xaiguard/ui";

const mockFeatures = [
  { name: "tcp.flags.syn", value: 1.0, shap: 2.45, type: "push" as const },
  { name: "ip.src_rate_5m", value: 45000, shap: 1.82, type: "push" as const },
  { name: "http.req.body_len", value: 0, shap: 0.94, type: "push" as const },
  { name: "tcp.window_size", value: 65535, shap: 0.42, type: "push" as const },
  { name: "ip.dst_entropy", value: 2.1, shap: -0.15, type: "pull" as const },
];

const mockAttentionWeights = [
  { token: "GET", weight: 0.02 },
  { token: "/api", weight: 0.05 },
  { token: "/v1", weight: 0.05 },
  { token: "/login", weight: 0.85 },
  { token: "HTTP/1.1", weight: 0.01 },
  { token: "Host:", weight: 0.01 },
  { token: "api.example.com", weight: 0.01 }
];

export default function PredictionDetailsPage({ params }: { params: { id: string } }) {
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setTimeout(() => {
      setLoading(false);
    }, 800);
  }, []);

  return (
    <div className="p-6 max-w-7xl mx-auto flex flex-col gap-8">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <div className="flex items-center gap-3 mb-2">
            <h1 className="text-3xl font-bold tracking-tight text-foreground">Alert: {params.id.split("-")[0]}</h1>
            <SeverityBadge severity="CRITICAL" />
          </div>
          <p className="text-muted-foreground">Detected at 2026-09-08 14:32:01 UTC</p>
        </div>
        <div className="flex items-center gap-2">
          <button className="px-4 py-2 border border-border bg-background rounded-md shadow-sm text-sm font-medium hover:bg-muted transition-colors">
            Acknowledge
          </button>
          <button className="px-4 py-2 bg-rose-600 text-white rounded-md shadow-sm text-sm font-medium hover:bg-rose-700 transition-colors flex items-center gap-2">
            <Shield className="w-4 h-4" /> Block Source IP
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-1 flex flex-col gap-6">
          <div className="rounded-xl border border-border/50 bg-card shadow-sm p-5 flex flex-col gap-4">
            <h2 className="font-bold flex items-center gap-2">
              <AlertTriangle className="w-5 h-5 text-amber-500" />
              Threat Intel
            </h2>
            <div className="flex flex-col gap-3">
              <div className="flex justify-between items-center pb-2 border-b border-border/50">
                <span className="text-sm text-muted-foreground">Classification</span>
                <span className="font-semibold">Volumetric DDoS</span>
              </div>
              <div className="flex justify-between items-center pb-2 border-b border-border/50">
                <span className="text-sm text-muted-foreground">Confidence</span>
                <span className="font-semibold text-rose-500">98.5%</span>
              </div>
              <div className="flex justify-between items-center pb-2 border-b border-border/50">
                <span className="text-sm text-muted-foreground">Source IP</span>
                <span className="font-mono text-sm">192.168.1.105</span>
              </div>
              <div className="mt-2">
                <MitreBadge 
                  techniqueId="T1498" 
                  title="Network Denial of Service" 
                  description="Adversaries may perform Network Denial of Service (DoS) attacks to degrade or block the availability of services." 
                />
              </div>
            </div>
          </div>

          <div className="rounded-xl border border-border/50 bg-card shadow-sm p-5 flex flex-col gap-3 bg-gradient-to-br from-blue-500/5 to-purple-500/5">
            <h2 className="font-bold flex items-center gap-2 text-primary">
              <Zap className="w-5 h-5" />
              AI Explanation (NLG)
            </h2>
            {loading ? (
              <div className="animate-pulse space-y-2 mt-2">
                <div className="h-4 bg-muted rounded w-full"></div>
                <div className="h-4 bg-muted rounded w-5/6"></div>
                <div className="h-4 bg-muted rounded w-4/6"></div>
              </div>
            ) : (
              <p className="text-sm text-muted-foreground leading-relaxed">
                The <strong className="text-foreground">XGBoost-v2</strong> model flagged this traffic as <strong className="text-foreground">Volumetric DDoS</strong> with 98.5% confidence. 
                This decision was primarily driven by an abnormally high TCP SYN rate (<strong className="text-rose-500">45,000 req/5m</strong>), strongly indicating a SYN flood attack attempting to exhaust server resources.
              </p>
            )}
          </div>
        </div>

        <div className="lg:col-span-2 flex flex-col gap-6">
          <div className="rounded-xl border border-border/50 bg-card shadow-sm p-6 flex flex-col gap-4">
            <div className="flex justify-between items-center">
              <h2 className="font-bold flex items-center gap-2">
                <Activity className="w-5 h-5 text-blue-500" />
                SHAP Feature Importance
              </h2>
              <span className="text-xs text-muted-foreground bg-muted px-2 py-1 rounded-full">Local Explanation</span>
            </div>
            
            {loading ? (
              <div className="h-64 flex items-center justify-center text-muted-foreground animate-pulse">Computing SHAP values...</div>
            ) : (
              <div className="flex flex-col gap-4 mt-4">
                {mockFeatures.map((f, i) => (
                  <FeatureContributionBar
                    key={i}
                    feature={f.name}
                    contribution={f.shap}
                    type={f.type}
                  />
                ))}
              </div>
            )}
          </div>

          <div className="rounded-xl border border-border/50 bg-card shadow-sm p-6 flex flex-col gap-4">
            <div className="flex justify-between items-center">
              <h2 className="font-bold flex items-center gap-2">
                <Cpu className="w-5 h-5 text-purple-500" />
                Transformer Attention Map
              </h2>
              <span className="text-xs text-muted-foreground bg-muted px-2 py-1 rounded-full">Payload Analysis</span>
            </div>
            
            {loading ? (
              <div className="h-32 flex items-center justify-center text-muted-foreground animate-pulse">Generating attention map...</div>
            ) : (
              <div className="mt-2">
                <p className="text-sm text-muted-foreground mb-4">
                  The deep learning payload analyzer focused on the following tokens to determine malicious intent. Darker red indicates higher attention weight.
                </p>
                <div className="flex flex-wrap gap-1 p-4 bg-muted/30 rounded-lg border border-border/50 font-mono text-sm">
                  {mockAttentionWeights.map((t, i) => (
                    <span 
                      key={i} 
                      className="px-1.5 py-0.5 rounded transition-colors"
                      style={{ 
                        backgroundColor: `rgba(225, 29, 72, ${t.weight})`,
                        color: t.weight > 0.5 ? 'white' : 'inherit'
                      }}
                      title={`Weight: ${t.weight.toFixed(2)}`}
                    >
                      {t.token}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
          
        </div>
      </div>
    </div>
  );
}
