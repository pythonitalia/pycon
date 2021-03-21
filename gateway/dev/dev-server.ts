/// <reference path="../types.d.ts" />

import { ApolloServer } from "apollo-server";
import { getPort } from "./utils";
import { gateway } from "../gateway";
import { apolloHeadersPlugin } from "../plugins/apollo-headers";
import { formatCookiesForExpressPlugin } from "../plugins/format-cookies-express";
import { createContext } from "../context";

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
