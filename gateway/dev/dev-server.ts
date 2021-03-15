/// <reference path="../types.d.ts" />

import { ApolloServer } from "apollo-server";
import { getPort } from "./utils";
import { gateway } from "../gateway";
import { createPastaporto } from "../pastaporto";
import { apolloHeadersPlugin } from "../plugins/apollo-headers";
import { formatCookiesForExpressPlugin } from "../plugins/format-cookies-express";
import cookie from "cookie";

const server = new ApolloServer({
  gateway,
  subscriptions: false,
  plugins: [apolloHeadersPlugin(false), formatCookiesForExpressPlugin],
  context: async ({ req, res }) => {
    const cookieHeader = req.headers.cookie;
    let identity = null;
    let refreshToken = null;

    const context: { [key: string]: any } = {
      res,
      setCookies: new Array(),
      setHeaders: new Array(),
    };

    if (cookieHeader) {
      const cookies = cookie.parse(req.headers.cookie);
      identity = cookies["identity"];
      refreshToken = cookies["refreshIdentity"];
    }

    context.pastaporto = await createPastaporto(
      identity,
      refreshToken,
      context,
    );
    return context;
  },
});

server.listen({ port: getPort() }).then(({ url }) => {
  console.log(`🚀 Server ready at ${url}`);
});
