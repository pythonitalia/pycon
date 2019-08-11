"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const fannypack_1 = require("fannypack");
exports.theme = {
    webFontLoader: {
        google: {
            families: ["Roboto Mono:400,700", "Rubik"],
        },
    },
    global: {
        fontFamily: "'Roboto Mono', sans-serif",
        fallbackFontFamily: "sans-serif",
    },
    Button: {
        base: fannypack_1.css `
      border-radius: 100px;
      white-space: nowrap;
    `,
        disabled: fannypack_1.css `
      opacity: 0.2;
    `,
    },
    palette: {
        /* primary: "#0C67FF", */
        primary: "#0066FF",
        white: "#fff",
        /* whiteInverted: "#0C67FF", */
        whiteInverted: "#0066FF",
        text: "#333",
    },
};
exports.customTheme = {
    breakPoints: {
        mobile: "320px",
        tabletPortrait: "768px",
        tabletLandscape: "992px",
        desktop: "1200px",
    },
};
