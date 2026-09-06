import "./globals.css";

export const metadata = {
  title: "SOC Dashboard | XAI-Guard",
  description: "SOC Analyst Dashboard",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
