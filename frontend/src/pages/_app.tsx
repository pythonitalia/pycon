/** @jsxRuntime classic */

/** @jsx jsx */
import { ApolloProvider } from "@apollo/client";
import "@python-italia/pycon-styleguide/style";
import { useEffect } from "react";
import { createIntl, createIntlCache, RawIntlProvider } from "react-intl";
import { Box, Flex, jsx, ThemeProvider } from "theme-ui";

import Script from "next/script";

import { APOLLO_STATE_PROP_NAME, getApolloClient } from "~/apollo/client";
import { ErrorBoundary } from "~/components/error-boundary";
import { Footer } from "~/components/footer";
import { Header } from "~/components/header";
import { GlobalStyles } from "~/components/styles";
import { updateOlarkFields } from "~/helpers/olark";
import messages from "~/locale";
import { LocaleProvider, useCurrentLanguage } from "~/locale/context";
import { theme } from "~/theme";
import { SharedLanguageProvider } from "~/components/multilingual-input";

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

  useEffect(() => {
    const listener = () => {
      updateOlarkFields();
    };

    // Once Olark is loaded we try restoring the data
    window.addEventListener("olarkLoaded", listener);
    return () => {
      window.removeEventListener("olarkLoaded", listener);
    };
  }, []);

  const enableOlark = false;

  return (
    <ThemeProvider theme={theme}>
      {enableOlark && (
        <Script
          strategy="lazyOnload"
          dangerouslySetInnerHTML={{
            __html: `
(function(o,l,a,r,k,y){if(o.olark)return;
r="script";y=l.createElement(r);r=l.getElementsByTagName(r)[0];
y.async=1;y.src="//"+a;r.parentNode.insertBefore(y,r);
y=o.olark=function(){k.s.push(arguments);k.t.push(+new Date)};
y.extend=function(i,j){y("extend",i,j)};
y.identify=function(i){y("identify",k.i=i)};
y.configure=function(i,j){y("configure",i,j);k.c[i]=j};
k=y._={s:[],t:[+new Date],c:{},l:a};
})(window,document,"static.olark.com/jsclient/loader.js");
/* Add configuration calls below this comment */
olark.identify('1751-12112149-10-1389');
var olarkLoadedEvent = new Event('olarkLoaded');
window.dispatchEvent(olarkLoadedEvent);
`,
          }}
        />
      )}

      <ApolloProvider client={apolloClient}>
        <RawIntlProvider value={intl}>
          <SharedLanguageProvider>
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
          </SharedLanguageProvider>
        </RawIntlProvider>
      </ApolloProvider>
    </ThemeProvider>
  );
};

export default MyApp;
