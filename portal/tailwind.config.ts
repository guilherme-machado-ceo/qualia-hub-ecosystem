import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: ["class"],
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    container: {
      center: true,
      padding: "2rem",
      screens: {
        "2xl": "1400px",
      },
    },
    extend: {
      fontFamily: {
        sans: ['"Rajdhani"', 'sans-serif'],
        orbitron: ['"Orbitron"', 'sans-serif'],
      },
      colors: {
        'q-dark': '#0b0f14',
        'q-dark-2': '#1a092a',
        'q-neon-cyan': '#00FFFF',
        'q-neon-magenta': '#FF00FF',
        'q-neon-green': '#00FF88',
        'q-light': '#e6eef6',
      },
      boxShadow: {
        'neon-glow': '0 0 15px theme(colors.q-neon-cyan)',
      },
      keyframes: {
        "accordion-down": {
          from: { height: "0" },
          to: { height: "var(--radix-accordion-content-height)" },
        },
        "accordion-up": {
          from: { height: "var(--radix-accordion-content-height)" },
          to: { height: "0" },
        },
      },
      animation: {
        "accordion-down": "accordion-down 0.2s ease-out",
        "accordion-up": "accordion-up 0.2s ease-out",
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
};
export default config;