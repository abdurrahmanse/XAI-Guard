import "./globals.css";
import { Providers } from "./providers";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "XAI-Guard | Admin Console",
  description: "MLOps Administration and Model Registry",
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
