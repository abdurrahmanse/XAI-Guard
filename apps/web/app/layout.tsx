import "./globals.css";
import { Inter } from "next/font/google";
const inter = Inter({ subsets: ["latin"], variable: "--font-sans" });

import { ThemeProvider } from "../components/common/theme-provider";
import { Navbar } from "../components/common/navbar";
import { Activity } from "lucide-react";
import type { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = {
  title: "XAI-Guard | Enterprise Cyber Security",
  description: "Explainable AI for Threat Detection",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={inter.variable} suppressHydrationWarning>
      <body className="antialiased font-sans min-h-screen bg-background text-foreground font-sans selection:bg-primary/30 flex flex-col">
        <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
          <Navbar />
          
          {/* Page Content */}
          <main className="flex-1 flex flex-col">
            {children}
          </main>

          {/* Footer */}
          <footer className="border-t border-border/40 bg-card py-12 px-6">
            <div className="container mx-auto max-w-7xl grid grid-cols-2 md:grid-cols-4 gap-8">
              <div className="col-span-2">
                <div className="flex items-center gap-2 mb-4">
                  <Activity className="h-5 w-5 text-primary" />
                  <span className="font-bold text-lg">XAI-Guard</span>
                </div>
                <p className="text-sm text-muted-foreground max-w-sm">
                  The world's first multi-model threat detection platform combining perfect accuracy with human-readable SHAP explanations.
                </p>
              </div>
              <div>
                <h3 className="font-semibold mb-4">Product</h3>
                <ul className="space-y-2 text-sm text-muted-foreground">
                  <li><Link href="/" className="hover:text-foreground transition-colors">Platform</Link></li>
                  <li><Link href="/" className="hover:text-foreground transition-colors">Integrations</Link></li>
                  <li><Link href="/pricing" className="hover:text-foreground transition-colors">Pricing</Link></li>
                  <li><Link href="/" className="hover:text-foreground transition-colors">Changelog</Link></li>
                </ul>
              </div>
              <div>
                <h3 className="font-semibold mb-4">Company</h3>
                <ul className="space-y-2 text-sm text-muted-foreground">
                  <li><Link href="/about" className="hover:text-foreground transition-colors">About Us</Link></li>
                  <li><Link href="/about" className="hover:text-foreground transition-colors">Careers</Link></li>
                  <li><Link href="/about" className="hover:text-foreground transition-colors">Legal</Link></li>
                  <li><Link href="/contact" className="hover:text-foreground transition-colors">Contact</Link></li>
                </ul>
              </div>
            </div>
            <div className="container mx-auto max-w-7xl mt-12 pt-8 border-t border-border/40 text-sm text-muted-foreground flex flex-col md:flex-row justify-between items-center">
              <p>© 2026 XAI-Guard Enterprise. All rights reserved.</p>
              <div className="flex gap-4 mt-4 md:mt-0">
                <Link href="/" className="hover:text-foreground transition-colors">Privacy Policy</Link>
                <Link href="/" className="hover:text-foreground transition-colors">Terms of Service</Link>
              </div>
            </div>
          </footer>
        </ThemeProvider>
      </body>
    </html>
  );
}
