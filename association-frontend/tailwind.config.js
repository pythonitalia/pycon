const { colors: defaultColors } = require("tailwindcss/defaultTheme");

const colors = {
    ...defaultColors,
    ...{
        blue: {
            50: "#8ad1ef",
            100: "#72c8ec",
            200: "#5bbfe9",
            300: "#43b6e6",
            400: "#2cade3",
            500: "#15A4E0",
            600: "#15a4e0",
            700: "#1293c9",
            800: "#1083b3",
            900: "#0c6286",
            DEFAULT: "#15A4E0",
        },
    },
};

module.exports = {
    purge: ["./pages/**/*.ts", "./components/**/*.ts"],
    darkMode: false, // or 'media' or 'class'
    theme: {
        colors: colors,
        extend: {},
    },
    variants: {
        extend: {},
    },
    plugins: [],
};
