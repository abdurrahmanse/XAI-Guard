"use client";

import React, { useState } from "react";
import { ThemeToggle } from "./theme-toggle";
import { Activity, Menu, X } from "lucide-react";
import Link from "next/link";

export function Navbar() {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  return (
    <header className="sticky top-0 z-50 w-full border-b border-border/40 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="w-full max-w-7xl mx-auto flex h-16 items-center justify-between px-4 sm:px-6">
        <div className="flex items-center gap-2">
          <div className="bg-primary text-primary-foreground p-1.5 rounded-lg shadow-sm">
            <Activity className="h-5 w-5" />
          </div>
          <Link href="/" className="font-bold text-xl tracking-tight">XAI-Guard</Link>
        </div>
        
        <nav className="hidden md:flex items-center gap-8 text-sm font-medium text-muted-foreground">
          <Link href="/" className="hover:text-foreground transition-colors">Platform</Link>
          <Link href="/about" className="hover:text-foreground transition-colors">About Us</Link>
          <Link href="/pricing" className="hover:text-foreground transition-colors">Pricing</Link>
          <Link href="/contact" className="hover:text-foreground transition-colors">Contact</Link>
        </nav>

        <div className="flex items-center gap-4">
          <ThemeToggle />
          <div className="hidden sm:flex items-center gap-3">
            <Link href="/login" className="text-sm font-medium hover:underline">Log in</Link>
            <Link href="/signup" className="inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors bg-primary text-primary-foreground hover:bg-primary/90 h-9 px-4 shadow">Get Started</Link>
          </div>
          <button 
            className="md:hidden p-2 text-muted-foreground hover:text-foreground"
            onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
          >
            {isMobileMenuOpen ? <X className="w-5 h-5"/> : <Menu className="w-5 h-5"/>}
          </button>
        </div>
      </div>

      {/* Mobile Menu */}
      {isMobileMenuOpen && (
        <div className="md:hidden border-t border-border/40 bg-background px-4 py-6 flex flex-col gap-4 shadow-lg absolute w-full">
          <Link href="/" onClick={() => setIsMobileMenuOpen(false)} className="text-sm font-medium">Platform</Link>
          <Link href="/about" onClick={() => setIsMobileMenuOpen(false)} className="text-sm font-medium">About Us</Link>
          <Link href="/pricing" onClick={() => setIsMobileMenuOpen(false)} className="text-sm font-medium">Pricing</Link>
          <Link href="/contact" onClick={() => setIsMobileMenuOpen(false)} className="text-sm font-medium">Contact</Link>
          <hr className="my-2 border-border/40" />
          <Link href="/login" onClick={() => setIsMobileMenuOpen(false)} className="text-sm font-medium">Log in</Link>
          <Link href="/signup" onClick={() => setIsMobileMenuOpen(false)} className="inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors bg-primary text-primary-foreground h-10 w-full shadow mt-2">Get Started</Link>
        </div>
      )}
    </header>
  );
}
