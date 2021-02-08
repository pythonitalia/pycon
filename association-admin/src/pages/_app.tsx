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
  (ssrExchange) => ({
    url: "http://localhost:4001/graphql",
    exchanges: [dedupExchange, cacheExchange, ssrExchange, fetchExchange],
  }),
  { ssr: true },
)(App);
