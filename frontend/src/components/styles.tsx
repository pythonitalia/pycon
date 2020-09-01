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
      ".article h1, \
        .article h2, \
        .article h3, \
        .article h4, \
        .article h5, \
        .article h6, \
        .article p, \
        .article ol, \
        .article ul": {
        marginBottom: "1em",
      },
      ".article ol, .article ul, .article li": {
        paddingLeft: "1em",
      },
    })}
  />
);
