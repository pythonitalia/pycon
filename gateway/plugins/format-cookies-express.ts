const cookie = require("cookie");

export const formatCookiesForExpressPlugin = {
  requestDidStart() {
    return {
      willSendResponse(requestContext: any) {
        // Under express we can set multiple cookies
        // by just calling response.append
        // this plugin assumes we set the express response in the context
        // and can be used only under express, so in the local env only
        const { setCookies = [], res } = requestContext.context;
        // @ts-ignore
        setCookies.forEach(({ name, value, options }) =>
          res.append("Set-Cookie", cookie.serialize(name, value, options)),
        );
      },
    };
  },
};
