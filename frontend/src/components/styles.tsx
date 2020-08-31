/** @jsx jsx */
import { Global } from "@emotion/core";
import { jsx } from "theme-ui";

export const GlobalStyles = () => (
  <Global
    styles={(theme) => ({
      "*": {
        margin: 0,
        padding: 0,
      },
      ".article": {
        lineHeight: 1.6,
      },
      "h1, h2, h3, h4, h5, h6, p, ol, ul": {
        marginBottom: "1em",
      },
      "ol, ul, li": {
        paddingLeft: "1em",
      },
    })}
  />
);
