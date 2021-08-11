import cookie from "cookie";
import { GraphQLResponse } from "graphql-request/dist/types";

import { ApolloContext } from "../context";

export type RequestContext = {
  context: ApolloContext;
  response: GraphQLResponse;
};

export const apolloHeadersPlugin = (applyCookies = false) => {
  return {
    requestDidStart() {
      return {
        willSendResponse(requestContext: RequestContext) {
          const { setHeaders = [], setCookies = [] } = requestContext.context;

          // inform user about wrong usage
          if (!Array.isArray(requestContext.context.setHeaders)) {
            console.warn("setHeaders is not in context or is not an array");
          }
          if (!Array.isArray(requestContext.context.setCookies)) {
            console.warn("setCookies is not in context or is not an array");
          }

          // set headers
          setHeaders.forEach(({ key, value }) => {
            requestContext.response.http.headers.append(key, value);
          });

          if (applyCookies) {
            // set cookies
            const serializedCookieArray = setCookies.map(
              ({ name, value, options }) =>
                cookie.serialize(name, value, options),
            );

            requestContext.response.http.headers.set(
              "Set-Cookie",
              JSON.stringify(serializedCookieArray),
            );
          }
          return requestContext;
        },
      };
    },
  };
};
