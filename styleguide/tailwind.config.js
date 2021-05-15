module.exports = {
  purge: ["./src/**/*.{js,jsx,ts,tsx,vue}"],
  mode: "jit",
  darkMode: false,
  theme: {
    fontFamily: {
      sans: ["aktiv-grotesk-extended", "ui-sans", "system-ui"],
      mono: ["Source Code Pro", "Menlo", "Consolas", "Monaco", "monospace"],
      display: ["aktiv-grotesk-extended"],
      body: ["aktiv-grotesk-extended"],
    },
    colors: {
      transparent: "transparent",
      current: "currentColor",
      white: "white",
      black: "black",
      orange: "#F17A5D",
      keppel: "#34B4A1",
      casablanca: "#F8B03D",
      aquamarine: "#79CDE0",
      "cornflower-blue": "#6A80EF",
      pink: "#DD9BC7",
      purple: "#9473B0",
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
