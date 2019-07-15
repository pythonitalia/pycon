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
    `,
    disabled: css`
      opacity: 0.2;
    `,
  },
  palette: {
    primary: "#0C67FF",
  },
};
