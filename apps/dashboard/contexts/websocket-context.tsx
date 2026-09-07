"use client";

import React, { createContext, useContext, useEffect, useState } from 'react';
import ReconnectingWebSocket from 'reconnecting-websocket';
import { useAlertsStore } from '@/stores/alerts-store';

interface WebSocketContextValue {
  status: 'connecting' | 'connected' | 'disconnected';
}

const WebSocketContext = createContext<WebSocketContextValue>({ status: 'disconnected' });

export const WebSocketProvider = ({ children, token }: { children: React.ReactNode, token?: string }) => {
  const [status, setStatus] = useState<'connecting' | 'connected' | 'disconnected'>('disconnected');
  const prependAlert = useAlertsStore(state => state.prependAlert);

  useEffect(() => {
    if (!token) return;

    // Use reconnecting-websocket for resilience
    const wsUrl = `${process.env.NEXT_PUBLIC_API_URL?.replace('http', 'ws') || 'ws://localhost:8000'}/v1/alerts/ws?token=${token}`;
    const rws = new ReconnectingWebSocket(wsUrl, [], {
      maxReconnectionDelay: 5000,
      minReconnectionDelay: 1000,
      reconnectionDelayGrowFactor: 1.3,
    });

    rws.addEventListener('open', () => {
      setStatus('connected');
    });

    rws.addEventListener('close', () => {
      setStatus('disconnected');
    });

    rws.addEventListener('message', (event) => {
      try {
        const data = JSON.parse(event.data);
        if (data.type === 'new_alert' && data.alert) {
          prependAlert(data.alert);
        } else if (data.id && data.attack_type) {
          // Fallback parsing for raw alerts
          prependAlert(data);
        }
      } catch (err) {
        console.error("Failed to parse websocket message", err);
      }
    });

    return () => {
      rws.close();
    };
  }, [token, prependAlert]);

  return (
    <WebSocketContext.Provider value={{ status }}>
      {children}
    </WebSocketContext.Provider>
  );
};

export const useWebSocket = () => useContext(WebSocketContext);
