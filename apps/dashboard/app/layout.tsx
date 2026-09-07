import './globals.css';
import { Providers } from './providers';
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'XAI-Guard | SOC Dashboard',
  description: 'Explainable AI Threat Detection Platform',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className="bg-background text-foreground selection:bg-primary/30">
        <Providers>
          {children}
        </Providers>
      </body>
    </html>
  );
}
