import React from "react";

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
          <link rel="preconnect" href="https://fonts.gstatic.com" />
          <link
            href="https://fonts.googleapis.com/css2?family=Lato:wght@400;700&display=swap"
            rel="stylesheet"
          />
        </Head>
        <body>
          <Main />
          <NextScript />
        </body>
      </Html>
    );
  }
}
