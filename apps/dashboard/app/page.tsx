import { AlertTriangle, Activity, ShieldAlert, Terminal } from "lucide-react";
import { ThemeToggle } from "../components/common/theme-toggle";

export default function DashboardHome() {
  return (
    <div className="min-h-screen bg-background font-sans p-8">
      <div className="max-w-7xl mx-auto space-y-8">
        
        <div className="flex items-center justify-between space-y-2">
          <div>
            <h2 className="text-3xl font-bold tracking-tight text-foreground flex items-center gap-2">
              <ShieldAlert className="w-7 h-7 text-destructive" />
              SOC Dashboard
            </h2>
            <p className="text-muted-foreground mt-1">Real-time threat monitoring and XAI explanations.</p>
          </div>
          <div className="flex items-center space-x-2">
            <ThemeToggle />
            <button className="inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 bg-primary text-primary-foreground hover:bg-primary/90 h-10 px-4 py-2">
              Download Report
            </button>
          </div>
        </div>

        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          <div className="rounded-xl border bg-card text-card-foreground shadow-sm">
            <div className="p-6 flex flex-row items-center justify-between space-y-0 pb-2">
              <h3 className="tracking-tight text-sm font-medium">Active Alerts</h3>
              <AlertTriangle className="h-4 w-4 text-destructive" />
            </div>
            <div className="p-6 pt-0">
              <div className="text-2xl font-bold">12</div>
              <p className="text-xs text-muted-foreground">+3 since last hour</p>
            </div>
          </div>

          <div className="rounded-xl border bg-card text-card-foreground shadow-sm">
            <div className="p-6 flex flex-row items-center justify-between space-y-0 pb-2">
              <h3 className="tracking-tight text-sm font-medium">Model Confidence</h3>
              <Activity className="h-4 w-4 text-muted-foreground" />
            </div>
            <div className="p-6 pt-0">
              <div className="text-2xl font-bold">98.2%</div>
              <p className="text-xs text-muted-foreground">Champion Model: XGBoost</p>
            </div>
          </div>

          <div className="rounded-xl border bg-card text-card-foreground shadow-sm md:col-span-2">
            <div className="p-6 flex flex-row items-center justify-between space-y-0 pb-2">
              <h3 className="tracking-tight text-sm font-medium">Events Analyzed</h3>
              <Terminal className="h-4 w-4 text-muted-foreground" />
            </div>
            <div className="p-6 pt-0">
              <div className="text-2xl font-bold">1,403,294</div>
              <p className="text-xs text-muted-foreground">Past 24 hours</p>
            </div>
          </div>
        </div>

        <div className="rounded-xl border bg-card text-card-foreground shadow-sm">
          <div className="flex flex-col space-y-1.5 p-6">
            <h3 className="font-semibold leading-none tracking-tight">Live Event Stream</h3>
            <p className="text-sm text-muted-foreground">Monitoring inbound network traffic.</p>
          </div>
          <div className="p-6 pt-0">
            <div className="h-[300px] w-full rounded-md border border-dashed flex items-center justify-center bg-muted/20">
              <span className="text-sm text-muted-foreground">Chart / Data Table goes here</span>
            </div>
          </div>
        </div>

      </div>
    </div>
  );
}
