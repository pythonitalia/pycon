import { ApolloServer } from "apollo-server-lambda";
import { createPastaporto } from "./pastaporto";
import { gateway } from "./gateway";
import httpHeadersPlugin from "apollo-server-plugin-http-headers";
import cookie from "cookie";

const server = new ApolloServer({
  gateway,
  subscriptions: false,
  plugins: [httpHeadersPlugin],
  context: async ({ event }) => {
    const cookieHeader = event.headers["cookie"];
    let identity = null;

    if (cookieHeader) {
      const cookies = cookie.parse(event.headers["cookie"]);
      identity = cookies["identity"];
    }

    return {
      setCookies: new Array(),
      setHeaders: new Array(),
      pastaporto: await createPastaporto(identity),
    };
  },
});

exports.graphqlHandler = server.createHandler();
