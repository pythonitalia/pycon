/** @jsxRuntime classic */

/** @jsx jsx */
import { Global } from "@emotion/react";
import React from "react";
import { jsx } from "theme-ui";

export const GlobalStyles = (): React.ReactElement => (
  <Global
    styles={() => ({
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
        listStyleType: "disc",
      },
      ".article h1, .article h2, .article h3, .article h4, .article h5, .article h6":
        {
          fontWeight: "bold",
        },
      ".article h1": {
        fontSize: "2rem",
      },
      ".article h2": {
        fontSize: "1.5rem",
      },
      ".article h3": {
        fontSize: "1.1rem",
      },
      ".article h4": {
        fontSize: "1rem",
      },
      ".article h5": {
        fontSize: "0.8rem",
      },
      ".article h6": {
        fontSize: "0.8rem",
      },
      ".article img": {
        width: "500px",
      },
    })}
  />
);
