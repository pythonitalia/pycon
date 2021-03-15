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

let serverHandler: any = null;

const handleManyCookies = (headers: any = {}) => {
  if (headers["set-cookie"]) {
    try {
      const value = JSON.parse(headers["set-cookie"]);
      if (Array.isArray(value)) {
        return {
          multiValueHeaders: {
            ...headers,
            "set-cookie": value,
          },
        };
      }
    } catch (err) {
      return { headers };
    }
  }

  return { headers };
};

exports.graphqlHandler = async (event: any, context: any) => {
  if (serverHandler === null) {
    serverHandler = server.createHandler();
  }

  const response = await serverHandler(event, context);
  const { headers, ...responseData } = response;
  const newHeaders = handleManyCookies(headers);

  return {
    ...responseData,
    ...newHeaders,
  };
};
