import { ApolloServer } from "apollo-server-lambda";
import * as ServerlessSentry from "@sentry/serverless";
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
    const baseContext = await createContext(
      event.headers,
      event.headers["Cookie"],
    );
    console.log("create context, express:", express);
    return {
      ...baseContext,
      res: express.res,
    };
  },
});

// const manyCookiesMiddleware = (_req: any, res: any, next: () => void) => {
//   const { headers } = res;

//   // In Apollo server we can only set 1 set-cookie and nothing else
//   // so what we do is that we set in Set-Cookie a serialized JSON Array
//   // with all the cookies we want to set
//   // When the gateway is running under lambda, we need to de-serialize
//   // the cookies and use the specific "multiValueHeaders"
//   // key to send multiple set-cookie
//   if (headers["set-cookie"]) {
//     try {
//       const setCookie = headers["set-cookie"];
//       headers["set-cookie"] = null;
//       const value = JSON.parse(setCookie);
//       if (Array.isArray(value)) {
//         res.headers = headers;
//         res.multiValueHeaders = {
//           "Set-Cookie": value,
//         };
//       }
//     } catch (err) {
//       console.error(
//         'updating cookies to "multiValueHeaders" raised an error',
//         err,
//       );
//     }
//   }

//   next();
// };

let serverHandler: ReturnType<ApolloServer["createHandler"]> | null = null;

exports.graphqlHandler = ServerlessSentry.AWSLambda.wrapHandler(
  async (event: any, context: any) => {
    console.log("graphqlHandler", event, context);

    if (!serverHandler) {
      console.log("creating handler");
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
    console.log("processing request");

    try {
      // eslint-disable-next-line @typescript-eslint/ban-ts-comment
      // @ts-ignore
      const response = await serverHandler!(event, context, null);
      console.log("response", response);
      return response;
    } catch (e) {
      console.error("server handler error:", e);
    }
  },
);
