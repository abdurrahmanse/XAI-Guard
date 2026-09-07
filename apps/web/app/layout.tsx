import "./globals.css";
import { ThemeProvider } from "../components/common/theme-provider";

export const metadata = {
  title: "XAI-Guard",
  description: "Explainable AI Cybersecurity",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body suppressHydrationWarning>
        <ThemeProvider attribute="class" defaultTheme="system" enableSystem disableTransitionOnChange>
          {children}
        </ThemeProvider>
      </body>
    </html>
  );
}
