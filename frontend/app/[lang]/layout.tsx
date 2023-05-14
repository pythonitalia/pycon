"use client";

import { ApolloProvider } from "@apollo/client";
import {
  ApolloNextAppProvider,
  NextSSRInMemoryCache,
  SSRMultipartLink,
} from "@apollo/experimental-nextjs-app-support/ssr";
import { getMessagesForLocale } from "@python-italia/pycon-styleguide";
import "@python-italia/pycon-styleguide/custom-style";
import { createIntl, createIntlCache, RawIntlProvider } from "react-intl";

import { makeApolloClient } from "~/apollo/client";
import { getApolloClient } from "~/apollo/sc-client";
import { Footer } from "~/components/footer";
import { Header } from "~/components/header";
import { GlobalStyles } from "~/components/styles";
import messages from "~/locale";
import { LocaleProvider } from "~/locale/context";
import { Language } from "~/locale/languages";

import "../../src/global.css";

const intlCache = createIntlCache();

type Props = {
  children: React.ReactNode;
  params: { lang: Language };
};
const RootLayout = ({ children }: Props) => {
  const lang = "en";
  const apolloClient = getApolloClient({});
  const intl = createIntl(
    {
      locale: lang,
      messages: {
        ...messages[lang],
        ...getMessagesForLocale(lang),
      },
    },
    intlCache,
  );
  return (
    <html lang={lang}>
      <body className="bg-milk">
        <ApolloNextAppProvider makeClient={makeApolloClient}>
          <RawIntlProvider value={intl}>
            <LocaleProvider lang={lang}>
              <GlobalStyles />
              <Header />
              {children}
              <Footer />
            </LocaleProvider>
          </RawIntlProvider>
        </ApolloNextAppProvider>
      </body>
    </html>
  );
};

export default RootLayout;
