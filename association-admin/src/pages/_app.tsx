import { dedupExchange, cacheExchange, fetchExchange } from "@urql/core";
import { authExchange } from "@urql/exchange-auth";
import { RecoilRoot } from "recoil";

import { withUrqlClient } from "next-urql";
import Router from "next/router";

import { Drawer } from "~/components/drawer";
import { SearchBar } from "~/components/search-bar";
import { UserProvider } from "~/components/user-provider";

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
  (ssrExchange) => ({
    url: "/graphql",
    exchanges: [
      dedupExchange,
      cacheExchange,
      ssrExchange,
      authExchange({
        didAuthError({ error }) {
          return error.graphQLErrors.some(
            (e) => e.extensions.exception.message === "Unauthorized",
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
  }),
  { ssr: false },
)(App);
