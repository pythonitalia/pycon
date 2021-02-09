import { dedupExchange, cacheExchange, fetchExchange } from "@urql/core";
import { RecoilRoot } from "recoil";

import { withUrqlClient } from "next-urql";

import { Drawer } from "~/components/drawer";

import "tailwindcss/tailwind.css";

const App = ({ Component, pageProps }) => (
  <RecoilRoot>
    <div className="h-screen w-screen flex overflow-hidden bg-white">
      <Drawer />
      <Component {...pageProps} />
    </div>
  </RecoilRoot>
);

export default withUrqlClient(
  (ssrExchange, ctx) => {
    const hasToken =
      typeof localStorage !== "undefined" && !!localStorage.getItem("token");
    const headers = {};

    if (hasToken) {
      const token = localStorage.getItem("token");
      headers["Authorization"] = `Bearer ${token}`;
    }

    console.log("headers", headers);

    return {
      url: "/graphql",
      exchanges: [dedupExchange, cacheExchange, ssrExchange, fetchExchange],
      fetchOptions: {
        credentials: "include",
        headers,
      },
    };
  },
  { ssr: false },
)(App);
