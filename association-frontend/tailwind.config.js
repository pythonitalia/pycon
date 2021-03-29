const {
  colors: defaultColors,
  boxShadow: defaultBoxShadow,
} = require("tailwindcss/defaultTheme");

const colors = {
  ...defaultColors,
  ...{
    blue: {
      50: "#8ad1ef",
      100: "#72c8ec",
      200: "#5bbfe9",
      300: "#43b6e6",
      400: "#2cade3",
      500: "#14A9E7",
      600: "#15a4e0",
      700: "#1293c9",
      800: "#1083b3",
      900: "#0c6286",
      DEFAULT: "#14A9E7",
    },
    bluecyan: "#0b59d6",
    yellow: "#ffc80a",
  },
};

module.exports = {
  purge: ["./src/pages/**/*.ts", "./components/**/*.ts"],
  darkMode: false, // or 'media' or 'class'
  theme: {
    colors: colors,
    fontFamily: {
      sans: ["Montserrat", "sans-serif"],
    },
    boxShadow: {
      ...defaultBoxShadow,
      solidblue: "-0.5em 0.5em 0 0 #0b59d6",
      solidyellow: "-0.5em 0.5em 0 0 #ffc80a",
    },
    extend: {
      backgroundImage: (theme) => ({
        "pycon-group": "url('/pycon_group7.jpg')",
        "pycon-group-blue": "url('/pycon-group-blue.jpg')",
        "white-background": "url('/white-background.jpg')",
      }),
    },
  },
  variants: {
    extend: {},
  },
  plugins: [],
};
