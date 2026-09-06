import "./globals.css";

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
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
