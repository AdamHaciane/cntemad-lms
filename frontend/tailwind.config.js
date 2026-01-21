/** @type {import('tailwindcss').Config} */
export default {
  presets: [require('frappe-ui/src/tailwind.config')],
  content: [
    './index.html',
    './src/**/*.{vue,js,ts,jsx,tsx}',
    './node_modules/frappe-ui/src/components/**/*.{vue,js}',
  ],
  theme: {
    extend: {
      colors: {
        // CNTEMAD brand colors
        cntemad: {
          primary: '#1e40af', // Bleu CNTEMAD
          secondary: '#059669', // Vert
          accent: '#dc2626', // Rouge Madagascar
        },
      },
    },
  },
  plugins: [],
}
