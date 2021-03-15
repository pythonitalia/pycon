import { ApolloServer } from "apollo-server-lambda";
import { createPastaporto } from "./pastaporto";
import { gateway } from "./gateway";
import { apolloHeadersPlugin } from "./plugins/apollo-headers";
import cookie from "cookie";

const server = new ApolloServer({
  gateway,
  subscriptions: false,
  introspection: true,
  plugins: [apolloHeadersPlugin(true)],
  context: async ({ event }) => {
    const cookieHeader = event.headers["cookie"];
    let identity = null;
    let refreshToken = null;

    const context: { [key: string]: any } = {
      setCookies: new Array(),
      setHeaders: new Array(),
    };

    if (cookieHeader) {
      const cookies = cookie.parse(event.headers["cookie"]);
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
