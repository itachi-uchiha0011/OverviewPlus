/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        brand: {
          DEFAULT: '#1976d2',
          dark: '#115293',
          light: '#63a4ff'
        }
      }
    }
  },
  darkMode: 'class',
  plugins: []
}