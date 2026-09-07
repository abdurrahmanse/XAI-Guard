import { create } from 'zustand';

interface Alert {
  id: string;
  source_ip: string;
  destination_ip: string;
  attack_type: string;
  severity: 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW';
  confidence: number;
  alert_count: number;
  last_seen_at: string;
  mitre_technique_id?: string;
  mitre_tactic_name?: string;
}

interface AlertsState {
  alerts: Alert[];
  selectedAlert: Alert | null;
  addAlerts: (newAlerts: Alert[]) => void;
  prependAlert: (alert: Alert) => void;
  setSelectedAlert: (alert: Alert | null) => void;
  updateAlert: (id: string, updates: Partial<Alert>) => void;
}

export const useAlertsStore = create<AlertsState>((set) => ({
  alerts: [],
  selectedAlert: null,
  addAlerts: (newAlerts) => set((state) => ({ alerts: [...state.alerts, ...newAlerts] })),
  prependAlert: (alert) => set((state) => ({ alerts: [alert, ...state.alerts] })),
  setSelectedAlert: (alert) => set({ selectedAlert: alert }),
  updateAlert: (id, updates) => set((state) => ({
    alerts: state.alerts.map(a => a.id === id ? { ...a, ...updates } : a)
  })),
}));
