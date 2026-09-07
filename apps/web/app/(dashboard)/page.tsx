"use client";

import { useEffect, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { AlertCircle, ShieldAlert, Activity } from "lucide-react";

export default function DashboardHome() {
  const [alerts, setAlerts] = useState<any[]>([]);

  // Mock initial load (fallback from react-query)
  const { data: initialAlerts, isLoading } = useQuery({
    queryKey: ["alerts"],
    queryFn: async () => [
      { id: "1", attack_type: "DDOS", severity: "CRITICAL", source_ip: "192.168.1.100", confidence: 0.98, timestamp: new Date().toISOString() },
      { id: "2", attack_type: "BRUTE_FORCE", severity: "HIGH", source_ip: "10.0.0.5", confidence: 0.85, timestamp: new Date().toISOString() },
    ]
  });

  useEffect(() => {
    if (initialAlerts) {
      setAlerts(initialAlerts);
    }
  }, [initialAlerts]);

  // Connect WebSocket
  useEffect(() => {
    // In real app, connect to ws://localhost:8000/v1/alerts/ws
    // Mocking websocket events for UI demonstration
    const interval = setInterval(() => {
      setAlerts(prev => [
        {
          id: Math.random().toString(),
          attack_type: ["PORT_SCAN", "WEB_ATTACK", "INFILTRATION"][Math.floor(Math.random() * 3)],
          severity: ["LOW", "MEDIUM", "HIGH"][Math.floor(Math.random() * 3)],
          source_ip: `10.0.0.${Math.floor(Math.random() * 255)}`,
          confidence: 0.6 + (Math.random() * 0.3),
          timestamp: new Date().toISOString()
        },
        ...prev.slice(0, 49) // Keep last 50
      ]);
    }, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="p-8">
      <div className="mb-8 flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-foreground">Live SOC Feed</h1>
          <p className="text-muted-foreground mt-1">Real-time intrusion detection alerts</p>
        </div>
        <div className="flex items-center space-x-2 text-sm text-primary">
          <Activity className="h-4 w-4 animate-pulse" />
          <span>Live via WebSocket</span>
        </div>
      </div>

      <div className="grid gap-4">
        {isLoading ? (
          <div className="h-24 rounded-lg border border-border bg-card animate-pulse" />
        ) : alerts.map((alert) => (
          <div key={alert.id} className="flex items-center justify-between rounded-lg border border-border bg-card p-4 shadow-sm transition-all hover:border-primary/50">
            <div className="flex items-center space-x-4">
              <div className={`p-2 rounded-full ${alert.severity === 'CRITICAL' ? 'bg-[#ff0000]/20 text-[#ff0000]' : alert.severity === 'HIGH' ? 'bg-[#ff8800]/20 text-[#ff8800]' : 'bg-[#00aaff]/20 text-[#00aaff]'}`}>
                {alert.severity === 'CRITICAL' ? <ShieldAlert className="h-6 w-6" /> : <AlertCircle className="h-6 w-6" />}
              </div>
              <div>
                <h3 className="text-lg font-semibold">{alert.attack_type.replace('_', ' ')}</h3>
                <p className="text-sm text-muted-foreground">Source: <span className="font-mono">{alert.source_ip}</span></p>
              </div>
            </div>
            
            <div className="text-right">
              <div className="inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold" style={{
                borderColor: alert.severity === 'CRITICAL' ? '#ff0000' : 'transparent',
                backgroundColor: alert.severity === 'CRITICAL' ? 'transparent' : 'var(--accent)',
                color: alert.severity === 'CRITICAL' ? '#ff0000' : 'var(--foreground)'
              }}>
                {alert.severity} ({(alert.confidence * 100).toFixed(1)}%)
              </div>
              <p className="mt-1 text-xs text-muted-foreground">
                {new Date(alert.timestamp).toLocaleTimeString()}
              </p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
