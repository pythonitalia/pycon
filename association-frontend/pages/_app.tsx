import { authExchange } from "@urql/exchange-auth";
import { getToken } from "hooks/use-login";
import {
  cacheExchange,
  dedupExchange,
  fetchExchange,
  makeOperation,
} from "urql";

import { withUrqlClient } from "next-urql";
import { Router } from "next/router";

import Footer from "~/components/footer/footer";
import Header from "~/components/header/header";
import { UserProvider } from "~/components/user-provider";

import "styles/globals.css";
import "tailwindcss/tailwind.css";

type AuthState = {
  token?: string;
};

const MyApp = ({ Component, pageProps, resetUrqlClient }) => {
  return (
    <div>
      <UserProvider resetUrqlClient={resetUrqlClient}>
        <Header />
        <main>
          <Component {...pageProps} />
        </main>
        <Footer />
      </UserProvider>
    </div>
  );
};

export default withUrqlClient((_ssrExchange, ctx) => ({
  url: "/graphql",
  exchanges: [
    dedupExchange,
    cacheExchange,

    authExchange({
      didAuthError({ error }) {
        return error.graphQLErrors.some((e) => e.message === "Unauthorized");
      },
      async getAuth({ authState }: { authState?: AuthState }) {
        console.log(`getAuth!! ${authState}`);
        if (!authState) {
          const token = typeof window !== "undefined" && getToken();
          console.log({ token });
          if (token) {
            return { token };
          }

          return null;
        }

        if (typeof window !== "undefined") {
          Router.replace("/logout");
        }

        return null;
      },
      addAuthToOperation({
        authState,
        operation,
      }: {
        authState?: AuthState;
        operation: any;
      }) {
        console.log({ authState });
        if (!authState || !authState.token) {
          return operation;
        }

        const fetchOptions =
          typeof operation.context.fetchOptions === "function"
            ? operation.context.fetchOptions()
            : operation.context.fetchOptions || {};

        console.log(`include the token: ${authState.token}`);
        return makeOperation(operation.kind, operation, {
          ...operation.context,
          fetchOptions: {
            ...fetchOptions,
            credentials: "include",
            headers: {
              ...fetchOptions.headers,
              Authorization: `Bearer ${authState.token}`,
            },
          },
        });
      },
    }),
    fetchExchange,
  ],
}))(MyApp);
