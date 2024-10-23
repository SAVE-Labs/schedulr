/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./schedulr/**/*.{html,js}"],
  theme: {
    extend: {},
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
}
