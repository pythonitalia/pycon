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
    fontSize: {
      "2xs": ".5rem",
      xs: ".75rem",
      sm: ".875rem",
      base: "1rem",
      lg: "1.125rem",
      xl: "1.25rem",
      "2xl": "1.5rem",
      "3xl": "1.875rem",
      "4xl": "2.25rem",
      "5xl": "3rem",
      "6xl": "4rem",
      "7xl": "5rem",
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
      green: "#34B4A1",
      grey: "#c6c6c6",
    },
    extend: {
      animation: {
        "marquee-slow": "marquee 60s linear infinite",
        "marquee-medium": "marquee 20s linear infinite",
      },
      keyframes: {
        marquee: {
          "0%": { transform: "translateX(0%)" },
          "100%": { transform: "translateX(-100%)" },
        },
      },
      zIndex: {
        "-1": "-1",
      },
      screens: {
        ticket: { raw: "(min-height: 810px) and (min-width: 640px)" },
      },
      scale: {
        10000: "100",
      },
      padding: {
        xl: '32rem',
       }
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
