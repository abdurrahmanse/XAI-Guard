import os
import json

os.makedirs('packages/ui', exist_ok=True)
os.makedirs('apps/dashboard/src/store', exist_ok=True)
os.makedirs('apps/dashboard/src/lib', exist_ok=True)

# 8.1 Frontend Tech Stack Declaration
with open('packages/ui/package.json', 'w') as f:
    json.dump({
        "name": "@xaiguard/ui",
        "version": "1.0.0",
        "main": "index.ts",
        "dependencies": {
            "clsx": "^2.1.1",
            "tailwind-merge": "^2.3.0",
            "class-variance-authority": "^0.7.0",
            "lucide-react": "^0.378.0",
            "next-themes": "^0.3.0",
            "zod": "^3.23.8"
        },
        "peerDependencies": {
            "react": "^19.0.0",
            "react-dom": "^19.0.0"
        }
    }, f, indent=2)

with open('apps/dashboard/package.json', 'w') as f:
    json.dump({
        "name": "dashboard",
        "version": "1.0.0",
        "private": True,
        "scripts": {
            "dev": "next dev --port 3001",
            "build": "next build",
            "start": "next start",
            "lint": "next lint"
        },
        "dependencies": {
            "next": "15.0.0",
            "react": "^19.0.0",
            "react-dom": "^19.0.0",
            "@tanstack/react-query": "^5.35.0",
            "@tanstack/react-table": "^8.16.0",
            "@tanstack/react-virtual": "^3.4.0",
            "zustand": "^4.5.2",
            "react-hook-form": "^7.51.4",
            "@hookform/resolvers": "^3.3.4",
            "framer-motion": "^11.2.0",
            "recharts": "^2.12.7",
            "nuqs": "^1.19.0",
            "date-fns": "^3.6.0",
            "cmdk": "^1.0.0",
            "reconnecting-websocket": "^4.4.0",
            "@react-pdf/renderer": "^3.4.4",
            "@xaiguard/ui": "workspace:*",
            "@xaiguard/api-types": "workspace:*"
        },
        "devDependencies": {
            "typescript": "^5.4.5",
            "@types/node": "^20",
            "@types/react": "^18",
            "@types/react-dom": "^18",
            "postcss": "^8",
            "tailwindcss": "^3.4.1",
            "eslint": "^9.0.0"
        }
    }, f, indent=2)

# 8.2 Zustand Store Architecture
with open('apps/dashboard/src/store/preferences.ts', 'w') as f:
    f.write("""import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { immer } from 'zustand/middleware/immer';

interface PreferencesState {
  alertSoundEnabled: boolean;
  compactMode: boolean;
  explanationMethod: "SHAP" | "LIME";
  toggleSound: () => void;
  toggleCompactMode: () => void;
  setExplanationMethod: (method: "SHAP" | "LIME") => void;
}

export const usePreferencesStore = create<PreferencesState>()(
  persist(
    immer((set) => ({
      alertSoundEnabled: true,
      compactMode: false,
      explanationMethod: "SHAP",
      toggleSound: () => set((state) => { state.alertSoundEnabled = !state.alertSoundEnabled; }),
      toggleCompactMode: () => set((state) => { state.compactMode = !state.compactMode; }),
      setExplanationMethod: (method) => set((state) => { state.explanationMethod = method; })
    })),
    {
      name: 'xaiguard-preferences',
    }
  )
);
""")

with open('apps/dashboard/src/store/websocket.ts', 'w') as f:
    f.write("""import { create } from 'zustand';
import { immer } from 'zustand/middleware/immer';

type ConnectionStatus = "connecting" | "connected" | "disconnected" | "error";

interface WebSocketState {
  status: ConnectionStatus;
  lastError: string | null;
  reconnectAttempts: number;
  setStatus: (status: ConnectionStatus) => void;
  setError: (error: string | null) => void;
  incrementReconnect: () => void;
  resetReconnect: () => void;
}

export const useWebSocketStore = create<WebSocketState>()(
  immer((set) => ({
    status: "disconnected",
    lastError: null,
    reconnectAttempts: 0,
    setStatus: (status) => set((state) => { state.status = status; }),
    setError: (error) => set((state) => { state.lastError = error; }),
    incrementReconnect: () => set((state) => { state.reconnectAttempts += 1; }),
    resetReconnect: () => set((state) => { state.reconnectAttempts = 0; })
  }))
);
""")

# 8.3 TanStack Query Configuration
with open('apps/dashboard/src/lib/query-client.ts', 'w') as f:
    f.write("""import { QueryClient } from '@tanstack/react-query';
import { zodFetcher } from '@xaiguard/api-types';

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 30 * 1000, // 30 seconds
      retry: (attemptIndex, error) => {
        if (attemptIndex >= 3) return false;
        return true;
      },
      retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000),
      refetchOnWindowFocus: false,
      networkMode: 'offlineFirst',
    },
  },
});
""")

# 8.4 shadcn/ui Design System Setup
with open('packages/ui/tailwind.config.ts', 'w') as f:
    f.write("""import type { Config } from "tailwindcss";

const config = {
  darkMode: ["class"],
  content: [
    "./components/**/*.{ts,tsx}",
    "../../apps/dashboard/src/**/*.{ts,tsx}",
    "../../apps/admin/src/**/*.{ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        severity: {
          critical: "hsl(0 84% 60%)",
          high: "hsl(25 95% 53%)",
          medium: "hsl(48 96% 53%)",
          low: "hsl(217 91% 60%)",
        },
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        }
      },
    },
  },
  plugins: [],
} satisfies Config;

export default config;
""")

print("Successfully generated Phase 8: Frontend Application Architecture.")
