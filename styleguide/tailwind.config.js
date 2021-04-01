module.exports = {
  purge: ["./src/**/*.{js,jsx,ts,tsx,vue}"],
  darkMode: false,
  theme: {
    fontFamily: {
      sans: ["aktiv-grotesk-extended", "ui-sans", "system-ui"],
      mono: ["Source Code Pro", "Menlo", "Consolas", "Monaco", "monospace"],
      display: ["aktiv-grotesk-extended"],
      body: ["aktiv-grotesk-extended"],
    },
    extend: {},
  },
  variants: {
    extend: {},
  },
  plugins: [require("@tailwindcss/aspect-ratio")],
};
