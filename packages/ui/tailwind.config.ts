import type { Config } from "tailwindcss";

const config = {
  darkMode: ["class"],
  content: [
    "./components/**/*.{ts,tsx}",
    "../../apps/dashboard/src/**/*.{ts,tsx}",
    "../../apps/admin/src/**/*.{ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        severity: {
          critical: "hsl(0 84% 60%)",
          high: "hsl(25 95% 53%)",
          medium: "hsl(48 96% 53%)",
          low: "hsl(217 91% 60%)",
        },
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        }
      },
    },
  },
  plugins: [],
} satisfies Config;

export default config;
