import { dedupExchange, cacheExchange, fetchExchange } from "@urql/core";
import { authExchange } from "@urql/exchange-auth";
import { RecoilRoot } from "recoil";
import { makeOperation } from "urql";

import { withUrqlClient } from "next-urql";
import Router from "next/router";

import { Drawer } from "~/components/drawer";
import { SearchBar } from "~/components/search-bar";
import { UserProvider } from "~/components/user-provider";
import { getToken } from "~/hooks/use-user";

import "tailwindcss/tailwind.css";

type AuthState = {
  token?: string;
};

const App = ({ Component, pageProps, resetUrqlClient }) => (
  <RecoilRoot>
    <UserProvider resetUrqlClient={resetUrqlClient}>
      <div className="h-screen w-screen flex overflow-hidden bg-white">
        <Drawer />
        <div className="flex flex-col w-0 flex-1 overflow-hidden">
          <SearchBar />
          <Component {...pageProps} />
        </div>
      </div>
    </UserProvider>
  </RecoilRoot>
);

export default withUrqlClient(
  (ssrExchange, ctx) => ({
    url: "/graphql",
    exchanges: [
      dedupExchange,
      cacheExchange,
      ssrExchange,
      authExchange({
        didAuthError({ error }) {
          return error.graphQLErrors.some(
            (e) => e.extensions.code === "UNAUTHENTICATED",
          );
        },
        async getAuth({ authState }: { authState?: AuthState }) {
          if (!authState) {
            const token = typeof window !== "undefined" && getToken();

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
          if (!authState || !authState.token) {
            return operation;
          }

          const fetchOptions =
            typeof operation.context.fetchOptions === "function"
              ? operation.context.fetchOptions()
              : operation.context.fetchOptions || {};

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
  }),
  { ssr: false },
)(App);
