/** @jsx jsx */
import { ApolloProvider } from "@apollo/react-hooks";
import { getDataFromTree } from "@apollo/react-ssr";
import { CacheProvider } from "@emotion/core";
import * as Sentry from "@sentry/browser";
import { ColorModeProvider } from "@theme-ui/color-modes";
import ApolloClient from "apollo-boost";
import { cache } from "emotion";
import withApollo from "next-with-apollo";
import App from "next/app";
import { createIntl, createIntlCache, RawIntlProvider } from "react-intl";
import { Box, Flex, jsx, Styled, ThemeProvider } from "theme-ui";

import { getApolloClient } from "~/apollo/client";
import { ErrorBoundary } from "~/components/error-boundary";
import { Footer } from "~/components/footer";
import { Header } from "~/components/header";
import { globalStyles } from "~/components/styles";
import messages from "~/locale";
import { LocaleProvider } from "~/locale/context";
import theme from "~/theme";
const intlCache = createIntlCache();

Sentry.init({
  dsn: "https://20b5f103cbf04fb3879ed3b5c6e98439@sentry.io/1889254",
});

class MyApp extends App<{ apollo: ApolloClient<any> }> {
  componentDidCatch(error: any, errorInfo: any) {
    Sentry.withScope((scope) => {
      Object.keys(errorInfo).forEach((key) => {
        scope.setExtra(key, errorInfo[key]);
      });

      Sentry.captureException(error);
    });

    super.componentDidCatch(error, errorInfo);
  }

  render() {
    const { Component, pageProps, apollo, router } = this.props;
    const locale = (router.query.lang as "en" | "it") ?? "en";

    const intl = createIntl(
      {
        locale,
        messages: messages[locale],
      },
      intlCache,
    );

    return (
      <ApolloProvider client={apollo}>
        <CacheProvider value={cache}>
          <ThemeProvider theme={theme}>
            <RawIntlProvider value={intl}>
              <ColorModeProvider>
                <LocaleProvider lang={locale}>
                  <Styled.root>
                    {globalStyles}
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
                  </Styled.root>
                </LocaleProvider>
              </ColorModeProvider>
            </RawIntlProvider>
          </ThemeProvider>
        </CacheProvider>
      </ApolloProvider>
    );
  }
}

export default withApollo(getApolloClient, { getDataFromTree })(MyApp);
