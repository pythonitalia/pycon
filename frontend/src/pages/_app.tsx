/** @jsxRuntime classic */
/** @jsx jsx */
import { ApolloClient } from "@apollo/client/core";
import { getDataFromTree } from "@apollo/client/react/ssr";
import * as Sentry from "@sentry/node";
import { Integrations as TracingIntegrations } from "@sentry/tracing";
import App, { AppContext } from "next/app";
import { createIntl, createIntlCache, RawIntlProvider } from "react-intl";
import { Box, Flex, jsx, ThemeProvider } from "theme-ui";

import { getApolloClient } from "~/apollo/client";
import { ErrorBoundary } from "~/components/error-boundary";
import { Footer } from "~/components/footer";
import { Header } from "~/components/header";
import { GlobalStyles } from "~/components/styles";
import { URLContext } from "~/helpers/use-url";
import messages from "~/locale";
import { LocaleProvider } from "~/locale/context";
import { theme } from "~/theme";
const intlCache = createIntlCache();

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  integrations: [new TracingIntegrations.BrowserTracing()],
  tracesSampleRate: 0.2,
});

const isSocial = (path: string) => path.endsWith("/social");

class MyApp extends App<{
  host: string;
  path: string;
  err: any;
}> {
  componentDidCatch(error: any, errorInfo: any) {
    Sentry.withScope((scope) => {
      Object.keys(errorInfo).forEach((key) => {
        scope.setExtra(key, errorInfo[key]);
      });

      Sentry.captureException(error);
    });

    super.componentDidCatch(error, errorInfo);
  }

  static async getInitialProps(appContext: AppContext) {
    const appProps = await App.getInitialProps(appContext);
    const { req } = appContext.ctx;

    const host = req
      ? ((req as any).protocol || "https") + "://" + req.headers.host
      : null;
    const path = req ? req.url : null;

    return { ...appProps, host, path };
  }

  render() {
    const { Component, pageProps, router, host, path, err } = this.props;
    const locale = (router.query.lang as "en" | "it") ?? "en";

    const intl = createIntl(
      {
        locale,
        messages: messages[locale],
      },
      intlCache,
    );

    return (
      <ThemeProvider theme={theme}>
        <URLContext.Provider value={{ host, path }}>
          <RawIntlProvider value={intl}>
            <LocaleProvider lang={locale}>
              <GlobalStyles />
              {isSocial(router.pathname) ? (
                <Component {...pageProps} />
              ) : (
                <Flex
                  sx={{
                    flexDirection: "column",
                    minHeight: "100vh",
                  }}
                >
                  <Header />

                  <Box sx={{ mt: [100, 130] }}>
                    <ErrorBoundary>
                      <Component {...pageProps} err={err} />
                    </ErrorBoundary>
                  </Box>

                  <Footer />
                </Flex>
              )}
            </LocaleProvider>
          </RawIntlProvider>
        </URLContext.Provider>
      </ThemeProvider>
    );
  }
}

export default MyApp;
