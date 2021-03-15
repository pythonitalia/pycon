const cookie = require("cookie");

export const formatCookiesForExpressPlugin = {
  requestDidStart() {
    return {
      willSendResponse(requestContext: any) {
        const { setCookies = [] } = requestContext.context;
        // @ts-ignore
        setCookies.forEach(({ name, value, options }) =>
          requestContext.context.res.append(
            "Set-Cookie",
            cookie.serialize(name, value, options),
          ),
        );
      },
    };
  },
};
