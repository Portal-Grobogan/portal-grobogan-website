/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/templates/**/*.html",
    "./app/static/js/**/*.js",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: "#1A5C38",
          dark: "#134429",
          tint: "#E8F5EE",
        },
        accent: {
          DEFAULT: "#D4A017",
          tint: "#FBF3DC",
        },
        "site-bg": "#F8F9FA",
        charcoal: "#1A1A2E",
        "text-body": "#333333",
      },
      fontFamily: {
        display: ["Montserrat", "sans-serif"],
        body: ["Inter", "sans-serif"],
      },
      boxShadow: {
        card: "0 1px 3px rgba(0,0,0,0.08), 0 1px 2px rgba(0,0,0,0.06)",
        "card-hover": "0 4px 12px rgba(0,0,0,0.12)",
      },
    },
  },
  safelist: [
    "bg-yellow-100", "text-yellow-800",
    "bg-blue-100", "text-blue-800",
    "bg-green-100", "text-green-800",
    "bg-red-100", "text-red-800",
  ],
  plugins: [
    require("@tailwindcss/forms"),
    require("@tailwindcss/typography"),
    require("@tailwindcss/line-clamp"),
  ],
};
