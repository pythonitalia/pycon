/** @jsx jsx */
import { ApolloProvider } from "@apollo/react-hooks";
import { getDataFromTree } from "@apollo/react-ssr";
import * as Sentry from "@sentry/browser";
import { ApolloClient } from "apollo-client";
import withApollo from "next-with-apollo";
import App, { AppContext } from "next/app";
import { createIntl, createIntlCache, RawIntlProvider } from "react-intl";
import { Box, Flex, jsx, Styled, ThemeProvider } from "theme-ui";

import { getApolloClient } from "~/apollo/client";
import { ErrorBoundary } from "~/components/error-boundary";
import { Footer } from "~/components/footer";
import { Header } from "~/components/header";
import { globalStyles } from "~/components/styles";
import { URLContext } from "~/helpers/use-url";
import messages from "~/locale";
import { LocaleProvider } from "~/locale/context";
import theme from "~/theme";
const intlCache = createIntlCache();

Sentry.init({
  dsn: "https://20b5f103cbf04fb3879ed3b5c6e98439@sentry.io/1889254",
});

const isSocial = (path: string) => path.endsWith("/social");

class MyApp extends App<{
  apollo: ApolloClient<any>;
  host: string;
  path: string;
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
    const { Component, pageProps, apollo, router, host, path } = this.props;
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
          <ApolloProvider client={apollo}>
            <RawIntlProvider value={intl}>
              <LocaleProvider lang={locale}>
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
                        <Component {...pageProps} />
                      </ErrorBoundary>
                    </Box>

                    <Footer />
                  </Flex>
                )}
              </LocaleProvider>
            </RawIntlProvider>
          </ApolloProvider>
        </URLContext.Provider>
      </ThemeProvider>
    );
  }
}

export default withApollo(getApolloClient, { getDataFromTree })(MyApp);
