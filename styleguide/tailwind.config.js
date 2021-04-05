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
    extend: {
      animation: {
        marquee: "marquee 20s linear infinite",
      },
      keyframes: {
        marquee: {
          "0%": { transform: "translateX(0%)" },
          "100%": { transform: "translateX(-100%)" },
        },
      },
    },
  },
  variants: {
    extend: {},
  },
  plugins: [
    require("@tailwindcss/aspect-ratio"),
    require("tailwindcss-blend-mode")(),
  ],
};
