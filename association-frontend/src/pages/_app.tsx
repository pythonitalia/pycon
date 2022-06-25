/* eslint-disable @next/next/no-page-custom-font */

/* eslint-disable @next/next/google-font-display */
import { Provider as UrqlProvider, createClient } from "urql";

import Head from "next/head";

import { Hero } from "~/components/hero";
import { UserProvider } from "~/components/user-provider";
import { StripeProvider } from "~/hooks/use-stripe";

import "../styles.css";

const client = createClient({
  url: "/graphql",
  fetchOptions: {
    credentials: "include",
  },
});

const App = ({ Component, pageProps }) => {
  return (
    <UrqlProvider value={client}>
      <UserProvider>
        <StripeProvider>
          <Head>
            <title>Associazione Python Italia</title>
            <link rel="icon" href="/favicon.png" />
            <link
              href="https://fonts.googleapis.com/css?family=Montserrat:300,700"
              rel="stylesheet"
            />
          </Head>

          <Hero />
          <main>
            <Component {...pageProps} />
          </main>
        </StripeProvider>
      </UserProvider>
    </UrqlProvider>
  );
};

export default App;
