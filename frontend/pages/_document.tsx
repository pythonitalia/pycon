import { extractCritical } from "emotion-server";
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
  static async getInitialProps({ renderPage, req }: DocumentContext) {
    const page = await renderPage();
    const styles = extractCritical(page.html);

    // TODO: protocol
    const url = (req as any).protocol + "://" + req.headers.host + req.url;

    return { ...page, ...styles, url };
  }

  render() {
    return (
      <Html>
        <Head>
          <link rel="stylesheet" href="https://use.typekit.net/mbr7dqb.css" />
          <link rel="shortcut icon" href="/favicon.png" />

          <style
            data-emotion-css={this.props.ids.join(" ")}
            dangerouslySetInnerHTML={{ __html: this.props.css }}
          />

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
