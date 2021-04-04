import { ApolloServer } from "apollo-server";

import { createContext } from "../context";
import { gateway } from "../gateway";
import { apolloHeadersPlugin } from "../plugins/apollo-headers";
import { formatCookiesForExpressPlugin } from "../plugins/format-cookies-express";
import { getPort } from "./utils";

const server = new ApolloServer({
  gateway,
  subscriptions: false,
  plugins: [apolloHeadersPlugin(false), formatCookiesForExpressPlugin],
  context: async ({ req, res }) => {
    const context = await createContext(req.headers.cookie);
    return {
      ...context,
      res,
    };
  },
});

server.listen({ port: getPort() }).then(({ url }) => {
  console.log(`🚀 Server ready at ${url}`);
});
