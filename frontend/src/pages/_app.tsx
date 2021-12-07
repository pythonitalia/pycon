/** @jsxRuntime classic */

/** @jsx jsx */
import { ApolloProvider } from "@apollo/client";
import { createIntl, createIntlCache, RawIntlProvider } from "react-intl";
import { Box, Flex, jsx, ThemeProvider } from "theme-ui";

import { APOLLO_STATE_PROP_NAME, getApolloClient } from "~/apollo/client";
import { ErrorBoundary } from "~/components/error-boundary";
import { Footer } from "~/components/footer";
import { Header } from "~/components/header";
import { GlobalStyles } from "~/components/styles";
import messages from "~/locale";
import { LocaleProvider, useCurrentLanguage } from "~/locale/context";
import { theme } from "~/theme";

const intlCache = createIntlCache();

const isSocial = (path: string) => path.endsWith("/social");

const MyApp = (props) => {
  const { Component, pageProps, router, err } = props;
  const apolloClient = getApolloClient(props.pageProps[APOLLO_STATE_PROP_NAME]);
  const locale = useCurrentLanguage();

  const intl = createIntl(
    {
      locale,
      messages: messages[locale],
    },
    intlCache,
  );

  return (
    <ThemeProvider theme={theme}>
      <ApolloProvider client={apolloClient}>
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

                <Box>
                  <ErrorBoundary>
                    <Component {...pageProps} err={err} />
                  </ErrorBoundary>
                </Box>

                <Footer />
              </Flex>
            )}
          </LocaleProvider>
        </RawIntlProvider>
      </ApolloProvider>
    </ThemeProvider>
  );
};

export default MyApp;
