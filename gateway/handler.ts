import { ApolloServer } from "apollo-server-lambda";
import { gateway } from "./gateway";
import { apolloHeadersPlugin } from "./plugins/apollo-headers";
import { createContext } from "./context";

const server = new ApolloServer({
  gateway,
  subscriptions: false,
  introspection: true,
  plugins: [apolloHeadersPlugin(true)],
  context: async ({ event }) => {
    return createContext(event.headers["cookie"]);
  },
});

const handleManyCookies = (headers: any = {}) => {
  if (headers["set-cookie"]) {
    try {
      const setCookie = headers["set-cookie"];
      headers["set-cookie"] = null;
      const value = JSON.parse(setCookie);
      if (Array.isArray(value)) {
        return {
          headers,
          multiValueHeaders: {
            "Set-Cookie": value,
          },
        };
      }
    } catch (err) {
      console.error(
        'updating cookies to "multiValueHeaders" raised an error',
        err,
      );
      return { headers };
    }
  }

  return { headers };
};

exports.graphqlHandler = async (event: any, context: any) => {
  const serverHandler = server.createHandler();

  try {
    const response: any = await new Promise((resolve, reject) => {
      serverHandler(event, context, (err: any, response: any = {}) => {
        if (err) {
          reject(err);
          return;
        }

        resolve(response);
      });
    });

    const { headers, ...responseData } = response;
    const newHeaders = handleManyCookies(headers);

    return {
      ...responseData,
      ...newHeaders,
    };
  } catch (e) {
    console.error("server handler error:", e);
  }
};
