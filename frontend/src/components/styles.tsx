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
      body: {
        WebkitPrintColorAdjust: "exact !important",
        printColorAdjust: "exact !important",
      },
      ".article ol, .article ul, .article li": {
        listStyleType: "disc",
        listStylePosition: "inside",
      },
      ".article a": {
        color: "inherit",
      },
      ".article p, span": {
        fontSize: "1.25rem",
      },
      ".article li p": {
        display: "inline-block",
      },
    })}
  />
);
