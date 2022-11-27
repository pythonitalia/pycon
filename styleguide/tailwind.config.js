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

      purple: {
        light: '#835DB5',
        dark: '#AB79EB',
        DEFAULT: '#835DB5',
      },
      orange: {
        light: '#D27B55',
        dark: '#F88F62',
        DEFAULT: '#D27B55',
      },
      blue: {
        light: '#538AD4',
        dark: '#62A2F8',
        DEFAULT: '#538AD4',
      },
      green: {
        light: '#469F81',
        dark: '#57BF9C',
        DEFAULT: '#469F81',
      },
      yellow: {
        light: '#E4A239',
        dark: '#F8B03D',
        DEFAULT: '#E4A239',
      },

      pink: {
        light: '#D15591',
        dark: '#F862AA',
        DEFAULT: '#D15591',
      },

      red: {
        light: '#D75353',
        dark: '#F86262',
        DEFAULT: '#D75353',
      },

      black: {
        light: '#0E1116',
        DEFAULT: '#0E1116',
      },

      cream: {
        light: '#FAF5F3',
        DEFAULT: '#FAF5F3',
      },

      white: {
        light: '#FFFFFF',
        DEFAULT: '#FFFFFF',
      },

      grey: {
        50: {
          light: '#1A1D22',
          DEFAULT: '#1A1D22',
        },
        100: {
          light: '#26292D',
          DEFAULT: '#26292D',
        },
        300: {
          light: '#56585C',
          DEFAULT: '#56585C',
        },
        500: {
          light: '#87888B',
          DEFAULT: '#87888B',
        },
        700: {
          light: '#B7B8B9',
          DEFAULT: '#B7B8B9',
        },
        900: {
          light: '#E7E7E8',
          DEFAULT: '#E7E7E8',
        },
      },

    //   white: "white",
    //   black: "black",
    //   orange: "#F17A5D",
    //   keppel: "#34B4A1",
    //   casablanca: "#F8B03D",
    //   aquamarine: "#79CDE0",
    //   "cornflower-blue": "#6A80EF",
    //   pink: "#DD9BC7",
    //   purple: "#9473B0",
    //   green: "#34B4A1",
    //   grey: "#c6c6c6",
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
