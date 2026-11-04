const { colors } = require('./src/config-parts');

module.exports = {
  content: ["./src/**/*.{js,jsx,ts,tsx,vue}"],
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
      1: '1px',
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
      '4xl-fluid': 'clamp(2.9rem, 12vw, 7.5rem)', // 120px
    },
    colors,
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

        7.5: '1.875rem', // 30px
        128: '28.875rem', // 462px
        256: '36.875rem', // 590px
      },
      width: {
        "full-outside-container": 'calc(100% + var(--screen-side-width))',
        "scroller-item": 'calc(100% - 5rem)',
        separator: '3px',

        7.5: '1.875rem', // 30px
        14.8: '3.75rem' // 60px
      },
      margin: {
        0.6: '0.188rem', // 3px
        15: '3.75rem', // 60px
        "-full-outside-container": 'calc((100% + var(--screen-side-width)) * -1)'
      },
      maxWidth: {
        // + the padding of the container
        container: `${1280 + 16 * 2}px`,

        'container-small': `${600 + 16 * 2}px`,
        'container-medium': `${810 + 16 * 2}px`,
        'container-2md': `${950 + 16 * 2}px`,

        full: '100%',
      },
      gridTemplateColumns: {
        'cardpart-increments': '1fr 231px',
        'cardpart-options': '0.5fr 1fr',
        'cardpart-options-options': 'repeat(var(--num-of-options), 1fr) auto',
        'bottombar': '1fr auto',
      },
    },
  },
  plugins: [
    require("tailwindcss-blend-mode")(),
    require('@tailwindcss/typography'),
  ],
};
