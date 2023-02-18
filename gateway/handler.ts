import * as ServerlessSentry from "@sentry/serverless";
import { ApolloServer } from "apollo-server-lambda";

import "./init";

import { createContext } from "./context";
import { createGateway } from "./gateway";
import { initSentry, SentryPlugin } from "./plugins/sentry";

initSentry(true);

const server = new ApolloServer({
  gateway: createGateway(),
  introspection: true,
  plugins: [SentryPlugin(true)],
  context: async ({ event, express }) => {
    return createContext({
      allHeaders: event.headers,
      cookiesHeader: event.headers["Cookie"],
      res: express.res,
    });
  },
});

let serverHandler: ReturnType<ApolloServer["createHandler"]> | null = null;

exports.graphqlHandler = ServerlessSentry.AWSLambda.wrapHandler(
  async (event: any, context: any) => {
    if (!serverHandler) {
      serverHandler = server.createHandler({
        expressGetMiddlewareOptions: {
          cors: {
            credentials: true,
            methods: ["GET", "POST", "OPTIONS", "HEAD"],
            origin: [
              /python-italia\.vercel\.app$/,
              "http://localhost:3000",
              "https://associazione.python.it",
              "https://pycon.it",
              "https://studio.apollographql.com",
            ],
          },
        },
      });
    }

    try {
      // eslint-disable-next-line @typescript-eslint/ban-ts-comment
      // @ts-ignore
      return await serverHandler!(event, context, null);
    } catch (e) {
      console.error("server handler error:", e);
    }
  },
);
