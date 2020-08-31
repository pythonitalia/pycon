import Document, {
  DocumentContext,
  Head,
  Html,
  Main,
  NextScript,
} from "next/document";
import React from "react";
import { InitializeColorMode } from "theme-ui";

export default class MyDocument extends Document<{
  ids: string[];
  css: string;
  url: string;
}> {
  static async getInitialProps(ctx: DocumentContext) {
    const initialProps = await Document.getInitialProps(ctx);

    const host = ctx.req
      ? ((ctx.req as any).protocol || "https") + "://" + ctx.req.headers.host
      : null;

    const url = host + ctx.req.url;

    return { ...initialProps, url };
  }

  render() {
    return (
      <Html>
        <Head>
          <link rel="stylesheet" href="https://use.typekit.net/mbr7dqb.css" />
          <link rel="shortcut icon" href="/favicon.png" />

          <meta property="og:url" content={this.props.url} />
          <meta property="twitter:url" content={this.props.url} />
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
