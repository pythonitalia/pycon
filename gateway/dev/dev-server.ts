import { ApolloServer } from "apollo-server";

import "../init";

import { createContext } from "../context";
import { createGateway } from "../gateway";
import { apolloHeadersPlugin } from "../plugins/apollo-headers";
import { formatCookiesForExpressPlugin } from "../plugins/format-cookies-express";
import { initSentry, SentryPlugin } from "../plugins/sentry";
import { getPort } from "./utils";

initSentry(false);

const server = new ApolloServer({
  gateway: createGateway(),
  plugins: [
    SentryPlugin(false),
    apolloHeadersPlugin(false),
    formatCookiesForExpressPlugin,
  ],
  cors: {
    origin: [
      "http://localhost:3020",
      "http://localhost:3010",
      "http://localhost:3000",
      "https://studio.apollographql.com",
    ],
    credentials: true,
  },
  context: async ({ req, res }) => {
    return createContext({
      allHeaders: req.headers,
      cookiesHeader: req.headers.cookie,
      res,
    });
  },
});

server.listen({ port: getPort() }).then(({ url }) => {
  console.log(`🚀 Server ready at ${url}`);
});
