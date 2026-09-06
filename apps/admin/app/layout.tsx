import "./globals.css";

export const metadata = {
  title: "Platform Admin | XAI-Guard",
  description: "Platform Engineering Admin Panel",
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
