import type { Config } from 'tailwindcss'

export default {
  content: [
    "./app/**/*.{ts,tsx}",
    "./pages/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
    "./src/**/*.{ts,tsx}",
  ],
  theme: {
    extend: {
        keyframes: {
        marquee: {
            "0%": { transform: "translateX(0%)" },
            "100%": { transform: "translateX(-50%)" },
        },
        },
        animation: {
        marquee: "marquee 12s linear infinite",
        },
    },
  },
  plugins: [],
} satisfies Config