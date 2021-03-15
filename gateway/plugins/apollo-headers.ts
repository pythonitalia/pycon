const cookie = require("cookie");

export const apolloHeadersPlugin = (applyCookies: boolean = false) => {
  return {
    requestDidStart() {
      return {
        willSendResponse(requestContext: any) {
          const { setHeaders = [], setCookies = [] } = requestContext.context;

          // inform user about wrong usage
          if (!Array.isArray(requestContext.context.setHeaders)) {
            console.warn("setHeaders is not in context or is not an array");
          }
          if (!Array.isArray(requestContext.context.setCookies)) {
            console.warn("setCookies is not in context or is not an array");
          }

          // set headers
          // @ts-ignore
          setHeaders.forEach(({ key, value }) => {
            requestContext.response.http.headers.append(key, value);
          });

          if (applyCookies) {
            // set cookies
            const serializedCookieArray = setCookies.map(
              // @ts-ignore
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
