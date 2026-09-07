import "./globals.css";
import { ThemeProvider } from "../components/common/theme-provider";
import { ThemeToggle } from "../components/common/theme-toggle";
import { Activity, Menu } from "lucide-react";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "XAI-Guard | Enterprise Cyber Security",
  description: "Explainable AI for Threat Detection",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className="min-h-screen bg-background text-foreground font-sans selection:bg-primary/30 flex flex-col">
        <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
          {/* Navigation Bar */}
          <header className="sticky top-0 z-50 w-full border-b border-border/40 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
            <div className="container mx-auto max-w-7xl flex h-16 items-center justify-between px-4 sm:px-6">
              <div className="flex items-center gap-2">
                <div className="bg-primary text-primary-foreground p-1.5 rounded-lg shadow-sm">
                  <Activity className="h-5 w-5" />
                </div>
                <span className="font-bold text-xl tracking-tight">XAI-Guard</span>
              </div>
              
              <nav className="hidden md:flex items-center gap-8 text-sm font-medium text-muted-foreground">
                <a href="/" className="hover:text-foreground transition-colors">Platform</a>
                <a href="/about" className="hover:text-foreground transition-colors">About Us</a>
                <a href="/pricing" className="hover:text-foreground transition-colors">Pricing</a>
                <a href="/contact" className="hover:text-foreground transition-colors">Contact</a>
              </nav>

              <div className="flex items-center gap-4">
                <ThemeToggle />
                <div className="hidden sm:flex items-center gap-3">
                  <a href="/login" className="text-sm font-medium hover:underline">Log in</a>
                  <a href="/signup" className="inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors bg-primary text-primary-foreground hover:bg-primary/90 h-9 px-4 shadow">Get Started</a>
                </div>
                <button className="md:hidden p-2 text-muted-foreground hover:text-foreground"><Menu className="w-5 h-5"/></button>
              </div>
            </div>
          </header>

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
                  <li><a href="#" className="hover:text-foreground">Features</a></li>
                  <li><a href="#" className="hover:text-foreground">Integrations</a></li>
                  <li><a href="/pricing" className="hover:text-foreground">Pricing</a></li>
                  <li><a href="#" className="hover:text-foreground">Changelog</a></li>
                </ul>
              </div>
              <div>
                <h3 className="font-semibold mb-4">Company</h3>
                <ul className="space-y-2 text-sm text-muted-foreground">
                  <li><a href="/about" className="hover:text-foreground">About Us</a></li>
                  <li><a href="#" className="hover:text-foreground">Careers</a></li>
                  <li><a href="#" className="hover:text-foreground">Legal</a></li>
                  <li><a href="/contact" className="hover:text-foreground">Contact</a></li>
                </ul>
              </div>
            </div>
            <div className="container mx-auto max-w-7xl mt-12 pt-8 border-t border-border/40 text-sm text-muted-foreground flex flex-col md:flex-row justify-between items-center">
              <p>© 2026 XAI-Guard Enterprise. All rights reserved.</p>
              <div className="flex gap-4 mt-4 md:mt-0">
                <a href="#" className="hover:text-foreground">Privacy Policy</a>
                <a href="#" className="hover:text-foreground">Terms of Service</a>
              </div>
            </div>
          </footer>
        </ThemeProvider>
      </body>
    </html>
  );
}
