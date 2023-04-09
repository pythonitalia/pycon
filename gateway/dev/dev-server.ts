import { ApolloServer } from "apollo-server";

import "../init";

import { createContext } from "../context";
import { createGateway } from "../gateway";
import { initSentry, SentryPlugin } from "../plugins/sentry";
import { getPort } from "./utils";

initSentry(false);

const server = new ApolloServer({
  gateway: createGateway(),
  plugins: [SentryPlugin(false)],
  cors: {
    origin: [
      "http://localhost:3020",
      "http://localhost:3010",
      "http://localhost:3000",
      "http://localhost:3002",
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
