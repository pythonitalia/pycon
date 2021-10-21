import React from "react";
import { InitializeColorMode } from "theme-ui";

import Document, { Head, Html, Main, NextScript } from "next/document";

export default class MyDocument extends Document<{
  ids: string[];
  css: string;
  url: string;
}> {
  render() {
    return (
      <Html>
        <Head>
          <link rel="stylesheet" href="https://use.typekit.net/mbr7dqb.css" />
          <link rel="shortcut icon" href="/favicon.png" />

          <script
            async={true}
            defer={true}
            data-domain="pycon.it"
            src="https://plausible.io/js/plausible.js"
          />
        </Head>
        <body>
          <InitializeColorMode />
          <Main />
          <NextScript />
        </body>
      </Html>
    );
  }
}
