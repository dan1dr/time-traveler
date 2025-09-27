import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#6C63FF',
          dark: '#4E47D0',
        },
        accent: '#48D1CC',
        bg: '#0B1020',
        card: '#121A2A',
        muted: '#94A3B8'
      },
      boxShadow: {
        glow: '0 0 40px rgba(108, 99, 255, 0.3)'
      }
    },
  },
  plugins: [],
}
export default config


