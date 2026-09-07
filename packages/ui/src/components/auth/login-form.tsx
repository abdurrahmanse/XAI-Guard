"use client";

import React from "react";
import { Activity } from "lucide-react";

export function LoginForm({ appName, postLoginRoute }: { appName: string, postLoginRoute: string }) {
  return (
    <div className="w-full max-w-md bg-card border border-border/50 rounded-2xl shadow-xl overflow-hidden">
      <div className="p-6 sm:p-8">
        <div className="flex justify-center mb-8">
          <div className="w-12 h-12 rounded-xl bg-primary/10 flex items-center justify-center text-primary">
            <Activity className="w-6 h-6" />
          </div>
        </div>
        <h2 className="text-2xl font-bold text-center mb-2">Sign in to {appName}</h2>
        <p className="text-muted-foreground text-center mb-8 text-sm">Enter your credentials to access your account</p>
        
        <form className="space-y-4" onSubmit={(e) => { e.preventDefault(); window.location.href = postLoginRoute; }}>
          <div className="space-y-2">
            <label className="text-sm font-medium">Work Email</label>
            <input type="email" placeholder="admin@enterprise.com" className="w-full h-10 px-3 rounded-md border bg-background text-base sm:text-sm focus:outline-none focus:ring-2 focus:ring-primary" required />
          </div>
          <div className="space-y-2">
            <div className="flex justify-between items-center">
              <label className="text-sm font-medium">Password</label>
              <a href="#" className="text-xs text-primary hover:underline">Forgot password?</a>
            </div>
            <input type="password" placeholder="••••••••" className="w-full h-10 px-3 rounded-md border bg-background text-base sm:text-sm focus:outline-none focus:ring-2 focus:ring-primary" required />
          </div>
          <button type="submit" className="w-full h-10 bg-primary text-primary-foreground rounded-md text-sm font-medium hover:bg-primary/90 transition-colors shadow-sm">
            Sign In
          </button>
        </form>
      </div>
      <div className="bg-muted/30 p-4 text-center border-t border-border/50">
        <p className="text-xs text-muted-foreground">Secure Enterprise SSO is enabled for your organization.</p>
      </div>
    </div>
  );
}
