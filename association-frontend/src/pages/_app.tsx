import { authExchange } from "@urql/exchange-auth";
import { cacheExchange, dedupExchange, fetchExchange } from "urql";

import { withUrqlClient } from "next-urql";
import Head from "next/head";
import { Router } from "next/router";

import { Hero } from "~/components/hero";
import { UserProvider } from "~/components/user-provider";

import "tailwindcss/tailwind.css";

type AuthState = {
  token?: string;
};

const App = ({ Component, pageProps, resetUrqlClient }) => {
  return (
    <UserProvider resetUrqlClient={resetUrqlClient}>
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
    </UserProvider>
  );
};

export default withUrqlClient((ssrExchange) => ({
  url: "/graphql",
  exchanges: [
    dedupExchange,
    cacheExchange,
    ssrExchange,
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

        if (typeof window !== "undefined") {
          Router.replace("/logout");
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
  fetchOptions: {
    credentials: "include",
  },
}))(App);
