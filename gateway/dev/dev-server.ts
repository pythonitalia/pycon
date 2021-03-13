/// <reference path="../types.d.ts" />

import { ApolloServer } from "apollo-server";
import { getPort } from "./utils";
import { gateway } from "../gateway";
import { createPastaporto } from "../pastaporto";
import httpHeadersPlugin from "apollo-server-plugin-http-headers";
import cookie from "cookie";

const server = new ApolloServer({
  gateway,
  subscriptions: false,
  plugins: [httpHeadersPlugin],
  context: async ({ req }) => {
    const cookieHeader = req.headers.cookie;
    let identity = null;

    if (cookieHeader) {
      const cookies = cookie.parse(req.headers.cookie);
      identity = cookies["identity"];
    }

    return {
      setCookies: new Array(),
      setHeaders: new Array(),
      pastaporto: await createPastaporto(identity),
    };
  },
});

server.listen({ port: getPort() }).then(({ url }) => {
  console.log(`🚀 Server ready at ${url}`);
});
