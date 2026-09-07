import { cookies } from "next/headers";
import { WebSocketProvider } from "@/contexts/websocket-context";
import { AlertsFeed } from "@/components/alerts/AlertsFeed";
import { ThreatDetailPanel } from "@/components/alerts/ThreatDetailPanel";

export default async function Page() {
  const cookieStore = await cookies();
  const token = cookieStore.get("access_token")?.value;

  return (
    <WebSocketProvider token={token}>
      <div className="flex flex-col gap-6 sm:gap-8 animate-in fade-in slide-in-from-bottom-4 duration-1000 h-full">
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
          <div>
            <h2 className="text-3xl font-bold tracking-tight">Live Alerts</h2>
            <p className="text-muted-foreground mt-1">Real-time threat landscape analysis.</p>
          </div>
          <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-emerald-500/10 border border-emerald-500/20">
            <div className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></div>
            <span className="text-xs font-medium text-emerald-500">Connected to WebSocket</span>
          </div>
        </div>

        <div className="flex-1 min-h-0 relative">
          <AlertsFeed />
        </div>

        <ThreatDetailPanel />
      </div>
    </WebSocketProvider>
  );
}
