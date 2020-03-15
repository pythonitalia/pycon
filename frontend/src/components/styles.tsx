/** @jsx jsx */
import { css, Global } from "@emotion/core";
import { jsx } from "theme-ui";

const reset = css`
  * {
    margin: 0;
    padding: 0;
  }

  .article {
    line-height: 1.6;

    h1,
    h2,
    h3,
    h4,
    h5,
    h6,
    p,
    ol,
    ul {
      margin-bottom: 1em;
    }

    ol,
    ul,
    li {
      padding-left: 1em;
    }
  }
`;

export const globalStyles = <Global styles={reset} />;
