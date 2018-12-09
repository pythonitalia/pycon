import * as React from 'react';
import Document, { NextDocumentContext, Head, Main, NextScript } from 'next/document';
import { ServerStyleSheet } from 'styled-components';

export default class MyDocument extends Document {
  public static async getInitialProps(ctx: NextDocumentContext) {
    const sheet = new ServerStyleSheet();

    const originalRenderPage = ctx.renderPage;

    ctx.renderPage = () =>
      originalRenderPage((App: any) => (props: any) =>
        sheet.collectStyles(<App {...props} />),
      );

    const initialProps = await Document.getInitialProps(ctx);

    return {
      ...initialProps,
      styles: [...initialProps.styles, ...sheet.getStyleElement()],
    };
  }

  public render() {
    return (
      <html>
        <Head>
          <link
            href="https://fonts.googleapis.com/css?family=Roboto:400,700|Varela+Round"
            rel="stylesheet"
          />
        </Head>

        <Main />
        <NextScript />
      </html>
    );
  }
}
