module.exports = {
  purge: ["./src/**/*.{js,jsx,ts,tsx,vue}"],
  mode: "jit",
  darkMode: false,
  theme: {
    screens: {
      md: '599px',
      lg: '1023px',
      xl: '1440px',
    },
    fontFamily: {
      sans: ["GeneralSans-Variable", "ui-sans", "system-ui"],
      mono: ["JetBrainsMono", "Source Code Pro", "Menlo", "Consolas", "Monaco", "monospace"],
      display: ["GeneralSans-Variable"],
      body: ["GeneralSans-Variable"],
    },

    borderWidth: {
      DEFAULT: '3px',
      0: 0,
      3: '3px',
      4: '4px',
    },
    lineHeight: {
      0.5: '0.875rem', // 14px
      1: '1rem', // 16px
      2: '1.25rem', // 20px
      3: '1.375rem', // 22px
      4: '1.5rem', // 24px
      5: '1.625rem', // 26px
      6: '1.75rem', // 28px
      7: '1.875rem', // 30px
      8: '2rem', // 32px
      9: '2.25rem', // 36px
      10: '2.5rem', // 40px
      11: '3rem', // 48px
      12: '3.5rem', // 56px
      13: '4rem', // 64px
      14: '5rem', // 80px
      15: '6.375rem', // 102px
    },
    fontSize: {
      sm: '0.875rem', // 14px
      base: '1rem', // 16px
      md: '1.25rem', // 20px
      "2md": '1.5rem', // 24px
      "3md": '1.75rem', // 28px
      lg: '1.875rem', // 30px
      "2lg": '2.25rem', // 36px
      xl: '2.5rem', // 40px
      "2xl": '3.5rem', // 56px
      "3xl": '5rem', // 80px
      '4xl': '7.5rem', // 120px
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
      white: '#FAF5F3',
      grey: {
        900: '#1A1C21',
        700: '#494A4D',
        500: '#848384',
        250: '#BFBCBC',
        100: '#E2DEDD',
        50: '#EEEAE8',
      },
      milk: '#FAF5F3',
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
      },
      height: {
        separator: '3px',

        128: '28.875rem', // 462px
        256: '36.875rem', // 590px
      },
      width: {
        "full-outside-container": 'calc(100% + var(--screen-side-width))',
        "scroller-item": 'calc(100% - 5rem)',
      },
      margin: {
        0.6: '0.188rem', // 3px
        15: '3.75rem', // 60px
        "-full-outside-container": 'calc((100% + var(--screen-side-width)) * -1)'
      },
      maxWidth: {
        // 1280 + the padding of the container
        container: `${1280 + 16 * 2}px`,
        full: '100%',
      },
      gridTemplateColumns: {
        'inverted-split-content-larger-content': 'max-content 1fr',
        'split-content-larger-content': '1fr max-content',
        'cardpart-increments': '1fr 231px',
        'cardpart-options': '0.5fr 1fr',
        'cardpart-options-inputs': '1fr 1fr 1fr 0.3fr',
        'bottombar': '1fr auto',
      },
    },
  },
  variants: {
    extend: {},
  },
  plugins: [
    require("tailwindcss-blend-mode")(),
  ],
};
