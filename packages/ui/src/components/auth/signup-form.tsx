import React from "react";
import { Activity } from "lucide-react";

export function SignupForm({ appName }: { appName: string }) {
  return (
    <div className="w-full max-w-md bg-card border border-border/50 rounded-2xl shadow-xl overflow-hidden">
      <div className="p-8">
        <div className="flex justify-center mb-8">
          <div className="w-12 h-12 rounded-xl bg-primary/10 flex items-center justify-center text-primary">
            <Activity className="w-6 h-6" />
          </div>
        </div>
        <h2 className="text-2xl font-bold text-center mb-2">Create an Account</h2>
        <p className="text-muted-foreground text-center mb-8 text-sm">Join {appName} to secure your enterprise infrastructure</p>
        
        <form className="space-y-4" onSubmit={(e) => { e.preventDefault(); window.location.href = '/login'; }}>
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <label className="text-sm font-medium">First Name</label>
              <input type="text" placeholder="John" className="w-full h-10 px-3 rounded-md border bg-background text-sm focus:outline-none focus:ring-2 focus:ring-primary" required />
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium">Last Name</label>
              <input type="text" placeholder="Doe" className="w-full h-10 px-3 rounded-md border bg-background text-sm focus:outline-none focus:ring-2 focus:ring-primary" required />
            </div>
          </div>
          <div className="space-y-2">
            <label className="text-sm font-medium">Work Email</label>
            <input type="email" placeholder="admin@enterprise.com" className="w-full h-10 px-3 rounded-md border bg-background text-sm focus:outline-none focus:ring-2 focus:ring-primary" required />
          </div>
          <div className="space-y-2">
            <label className="text-sm font-medium">Password</label>
            <input type="password" placeholder="••••••••" className="w-full h-10 px-3 rounded-md border bg-background text-sm focus:outline-none focus:ring-2 focus:ring-primary" required />
          </div>
          <button type="submit" className="w-full h-10 bg-primary text-primary-foreground rounded-md text-sm font-medium hover:bg-primary/90 transition-colors shadow-sm">
            Create Account
          </button>
        </form>
      </div>
      <div className="bg-muted/30 p-4 text-center border-t border-border/50">
        <p className="text-sm text-muted-foreground">Already have an account? <a href="/login" className="text-primary hover:underline font-medium">Sign in</a></p>
      </div>
    </div>
  );
}
