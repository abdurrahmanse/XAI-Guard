import { create } from 'zustand';
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
