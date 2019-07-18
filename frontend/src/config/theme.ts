import { css } from "fannypack";

export const theme = {
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
    base: css`
      border-radius: 100px;
      white-space: nowrap;
    `,
    disabled: css`
      opacity: 0.2;
    `,
  },
  palette: {
    primary: "#0C67FF",
    white: "#fff",
    whiteInverted: "#0C67FF",
    text: "#333",
  },
};

export const customTheme = {
  breakPoints: {
    mobile: "320px",
    tabletPortrait: "768px",
    tabletLandscape: "992px",
    desktop: "1200px",
  },
};
