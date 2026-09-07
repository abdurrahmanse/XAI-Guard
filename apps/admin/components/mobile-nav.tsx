"use client";

import React, { useState } from "react";
import { Menu, X, Database, LineChart, Shield, LayoutDashboard, LogOut, Settings } from "lucide-react";

export function MobileNav() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className="md:hidden">
      <button 
        onClick={() => setIsOpen(true)}
        className="p-2 -ml-2 mr-2 text-muted-foreground hover:text-foreground"
      >
        <Menu className="w-5 h-5" />
      </button>

      {isOpen && (
        <div className="fixed inset-0 z-50 flex">
          <div className="fixed inset-0 bg-background/80 backdrop-blur-sm" onClick={() => setIsOpen(false)} />
          <div className="fixed inset-y-0 left-0 w-64 bg-card border-r shadow-lg flex flex-col animate-in slide-in-from-left-2">
            <div className="h-16 flex items-center justify-between px-6 border-b">
              <div className="flex items-center">
                <Shield className="w-5 h-5 text-primary mr-2" />
                <span className="font-bold tracking-tight">Admin Console</span>
              </div>
              <button onClick={() => setIsOpen(false)} className="p-2 text-muted-foreground hover:text-foreground">
                <X className="w-5 h-5" />
              </button>
            </div>
            
            <div className="p-4 flex-1">
              <div className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-2 px-3">Management</div>
              <nav className="space-y-1">
                <a href="/" className="flex items-center gap-3 px-3 py-2 rounded-md text-sm hover:bg-accent text-muted-foreground hover:text-foreground" onClick={() => setIsOpen(false)}>
                  <LayoutDashboard className="w-4 h-4" /> Overview
                </a>
                <a href="/models" className="flex items-center gap-3 px-3 py-2 rounded-md text-sm bg-primary/10 text-primary font-medium" onClick={() => setIsOpen(false)}>
                  <Database className="w-4 h-4" /> Model Registry
                </a>
                <a href="/metrics" className="flex items-center gap-3 px-3 py-2 rounded-md text-sm hover:bg-accent text-muted-foreground hover:text-foreground" onClick={() => setIsOpen(false)}>
                  <LineChart className="w-4 h-4" /> System Metrics
                </a>
              </nav>
            </div>
            <div className="p-4 border-t">
              <nav className="space-y-1">
                <a href="/settings" className="flex items-center gap-3 px-3 py-2 rounded-md text-sm hover:bg-accent text-muted-foreground hover:text-foreground transition-colors" onClick={() => setIsOpen(false)}>
                  <Settings className="w-4 h-4" /> Config
                </a>
                <a href="/login" className="flex items-center gap-3 px-3 py-2 rounded-md text-sm hover:bg-destructive/10 text-destructive hover:text-destructive transition-colors" onClick={() => setIsOpen(false)}>
                  <LogOut className="w-4 h-4" /> Sign Out
                </a>
              </nav>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
