import { authExchange } from "@urql/exchange-auth";
import { cacheExchange, dedupExchange, fetchExchange } from "urql";

import { withUrqlClient } from "next-urql";
import Head from "next/head";

import { Hero } from "~/components/hero";
import { UserProvider } from "~/components/user-provider";
import { API_URL } from "~/helpers/config";
import { StripeProvider } from "~/hooks/use-stripe";

import "tailwindcss/tailwind.css";

type AuthState = {
  token?: string;
};

const App = ({ Component, pageProps, resetUrqlClient }) => {
  return (
    <UserProvider resetUrqlClient={resetUrqlClient}>
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
  );
};

export default withUrqlClient(
  (ssrExchange, ctx) => {
    return {
      url: API_URL,
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

            // if (typeof window !== "undefined") {
            //   // @ts-ignore
            //   Router.replace("/logout");
            // }

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
        ssrExchange,
        fetchExchange,
      ],
      fetchOptions: () => {
        const options: { [key: string]: string | object } = {
          credentials: "include",
        };

        if (ctx && ctx.req?.headers.cookie) {
          options.headers = {
            cookie: ctx.req!.headers.cookie,
          };
        }
        return options;
      },
    };
  },
  { ssr: true },
)(App);
