/* eslint-disable @next/next/no-page-custom-font */

/* eslint-disable @next/next/google-font-display */
import { authExchange } from "@urql/exchange-auth";
import {
  Provider as UrqlProvider,
  createClient,
  cacheExchange,
  dedupExchange,
  fetchExchange,
} from "urql";

import Head from "next/head";

import { Hero } from "~/components/hero";
import { UserProvider } from "~/components/user-provider";
import { StripeProvider } from "~/hooks/use-stripe";

import "tailwindcss/tailwind.css";

type AuthState = {
  token?: string;
};

const client = createClient({
  url: "/graphql",
  exchanges: [
    dedupExchange,
    cacheExchange,
    authExchange({
      didAuthError({ error }) {
        return error.graphQLErrors.some(
          (e) => e.message === "Not authenticated",
        );
      },
      async getAuth({ authState }: { authState?: AuthState }) {
        if (!authState) {
          return null;
        }

        return null;
      },
      addAuthToOperation({
        operation,
      }: {
        authState?: AuthState;
        operation: any;
      }) {
        return operation;
      },
    }),
    fetchExchange,
  ],
  fetchOptions: () => {
    const options: { [key: string]: string | { cookie: string } } = {
      credentials: "include",
    };
    return options;
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
