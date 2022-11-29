module.exports = {
  purge: ["./src/**/*.{js,jsx,ts,tsx,vue}"],
  mode: "jit",
  darkMode: false,
  theme: {
    fontFamily: {
      sans: ["GeneralSans-Variable", "ui-sans", "system-ui"],
      mono: ["JetBrainsMono", "Source Code Pro", "Menlo", "Consolas", "Monaco", "monospace"],
      display: ["GeneralSans-Variable"],
      body: ["GeneralSans-Variable"],
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

      // primary
      coral: {
        light: '#F17A5D',
        DEFAULT: '#F17A5D',
      },
      caramel: {
        light: '#EAD6CE',
        DEFAULT: '#EAD6CE',
      },
      cream: {
        light: '#FCE8DE',
        DEFAULT: '#FCE8DE',
      },

      // accent
      yellow: {
        light: '#F8B03D',
        DEFAULT: '#F8B03D',
      },
      green: {
        light: '#34B4A1',
        DEFAULT: '#34B4A1',
      },
      purple: {
        light: '#9473B0',
        DEFAULT: '#9473B0',
      },
      pink: {
        light: '#DD9BC7',
        DEFAULT: '#DD9BC7',
      },
      blue: {
        light: '#79CDE0',
        DEFAULT: '#79CDE0',
      },
      // status
      red: {
        light: '#D75353',
        DEFAULT: '#D75353',
      },
      success: {
        light: '#33BC8B',
        DEFAULT: '#33BC8B',
      },
      warning: {
        light: '#F8B03D',
        DEFAULT: '#F8B03D',
      },
      neutral: {
        light: '#538AD4',
        DEFAULT: '#538AD4',
      },

      // grey scale
      black: '#0E1116',
      white: '#FFFFFF',
      grey: {
        900: '#1A1C21',
        700: '#494A4D',
        500: '#848384',
        250: '#BFBCBC',
        100: '#E2DEDD',
        50: '#EEEAE8',
      },
      milk: '#A7A7A7',
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
