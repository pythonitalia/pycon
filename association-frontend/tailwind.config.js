module.exports = {
  content: ["./src/**/*.tsx"],
  darkMode: "media",
  theme: {
    fontFamily: {
      sans: ["Montserrat", "sans-serif"],
    },
    extend: {
      boxShadow: {
        solidblue: "-0.5em 0.5em 0 0 #0b59d6",
        solidyellow: "-0.5em 0.5em 0 0 #ffc80a",
      },
      colors: {
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
      backgroundImage: () => ({
        "pycon-group": "url('/pycon_group7.jpg')",
        "pycon-group-blue": "url('/pycon-group-blue.jpg')",
        "white-background": "url('/white-background.jpg')",
        "reception-desk-pycon-10": "url('/reception-desk-pycon-10.jpg')",
      }),
    },
  },
  plugins: [],
};
