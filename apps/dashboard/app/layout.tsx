import './globals.css';
import { Inter } from "next/font/google";
const inter = Inter({ subsets: ["latin"], variable: "--font-sans" });

import { Providers } from './providers';
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'XAI-Guard | SOC Dashboard',
  description: 'Explainable AI Threat Detection Platform',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={inter.variable} suppressHydrationWarning>
      <body className="antialiased font-sans bg-background text-foreground selection:bg-primary/30">
        <Providers>
          {children}
        </Providers>
      </body>
    </html>
  );
}
