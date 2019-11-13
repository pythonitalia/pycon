export default {
  space: [0, 4, 8, 16, 32, 64, 128, 256, 512],
  fonts: {
    body: "aktiv-grotesk-extended, sans-serif",
    heading: "inherit",
    monospace: "Menlo, monospace",
  },
  fontSizes: [12, 14, 16, 20, 24, 32, 48, 64, 96],
  fontWeights: {
    body: 400,
    heading: 500,
    bold: 700,
  },
  lineHeights: {
    body: 1.5,
    heading: 1.125,
  },
  sizes: {
    largeContainer: 1320,
    container: 1200,
  },
  colors: {
    text: "#000",
    background: "#fff",
    primary: "#07c",
    secondary: "#30c",
    muted: "#f6f6f6",
    purple: "#FA00FF",
    yellow: "#F8B03D",
    orange: "#F17A5D",
    violet: "#9473B0",
  },
  borders: {
    primary: "3px solid #000000",
  },
  buttons: {
    primary: {
      position: "relative",
      padding: [2, 3],

      fontSize: [0, 2],
      fontFamily: "body",
      fontWeight: "heading",

      mx: [1, 2, 3, 4],

      color: "#000",
      borderWidth: ["3px", "4px"],
      borderStyle: "solid",
      borderColor: "#000",
      background: "#F8B03D",
    },
    white: {
      variant: "buttons.primary",
      background: "#fff",
    },
  },
  links: {
    header: {
      color: "white",
      fontSize: 5,
      textDecoration: "none",
      "&:hover": {
        borderBottom: "2px solid white",
      },
    },
  },
  text: {
    caps: {
      textTransform: "uppercase",
    },
    header: {
      variant: "text.caps",
      fontSize: 2,
      fontWeight: "bold",
      mt: 20,
      mb: 3,
    },
    prefooter: {
      fontWeight: "bold",
      color: "violet",
    },
    heading: {
      fontFamily: "heading",
      fontWeight: "heading",
      lineHeight: "heading",
    },
    marquee: {
      variant: "text.caps",
      fontSize: 5,
      whiteSpace: "nowrap",
    },
  },
  styles: {
    root: {
      fontFamily: "body",
      lineHeight: "body",
      fontWeight: "body",
    },
    h1: {
      color: "text",
      fontFamily: "heading",
      lineHeight: "heading",
      fontWeight: "heading",
      mb: "1em",
      fontSize: 5,
    },
    h2: {
      color: "text",
      fontFamily: "heading",
      lineHeight: "heading",
      fontWeight: "heading",
      mb: "1em",
      fontSize: 4,
    },
    h3: {
      color: "text",
      fontFamily: "heading",
      lineHeight: "heading",
      fontWeight: "heading",
      mb: "1em",
      fontSize: 3,
    },
    h4: {
      color: "text",
      fontFamily: "heading",
      lineHeight: "heading",
      fontWeight: "heading",
      mb: "1em",
      fontSize: 2,
    },
    h5: {
      color: "text",
      fontFamily: "heading",
      lineHeight: "heading",
      fontWeight: "heading",
      mb: "1em",
      fontSize: 1,
    },
    h6: {
      color: "text",
      fontFamily: "heading",
      lineHeight: "heading",
      fontWeight: "heading",
      mb: "1em",
      fontSize: 0,
    },
    p: {
      color: "text",
      fontFamily: "body",
      fontWeight: "body",
      lineHeight: "body",
      mb: "1em",
    },
    a: {
      color: "primary",
    },
    pre: {
      fontFamily: "monospace",
      overflowX: "auto",
      code: {
        color: "inherit",
      },
    },
    code: {
      fontFamily: "monospace",
      fontSize: "inherit",
    },
    table: {
      width: "100%",
      borderCollapse: "separate",
      borderSpacing: 0,
    },
    th: {
      textAlign: "left",
      borderBottomStyle: "solid",
    },
    td: {
      textAlign: "left",
      borderBottomStyle: "solid",
    },
    img: {
      maxWidth: "100%",
    },
  },
  zIndices: {
    header: "10",
  },
};
