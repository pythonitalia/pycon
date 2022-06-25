module.exports = {
  content: ["./src/**/*.tsx"],
  darkMode: 'media',
  theme: {
    fontFamily: {
      sans: ["Montserrat", "sans-serif"],
    },
    extend: {
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
