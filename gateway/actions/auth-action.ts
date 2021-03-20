import {
  createIdentityToken,
  createRefreshToken,
} from "../pastaporto/identity";
import { IS_DEV } from "../config";
import { PastaportoAction } from "./entities";

type AuthOptions = {
  identityOnly?: boolean;
};

export class AuthAction extends PastaportoAction<AuthOptions> {
  async apply(context: any) {
    const sub = `${this.payload["id"]}`;
    const identityToken = createIdentityToken(sub);
    let refreshToken;

    // clear previous set cookies (clear identity cookies)
    context.setCookies.splice(0, context.setCookies.length);

    context.setCookies.push({
      name: "identity",
      value: identityToken,
      options: {
        httpOnly: true,
        maxAge: 60 * 15,
        path: "/",
        sameSite: true,
        secure: !IS_DEV,
      },
    });

    if (!this.options?.identityOnly) {
      refreshToken = createRefreshToken(sub);

      context.setCookies.push({
        name: "refreshIdentity",
        value: refreshToken,
        options: {
          httpOnly: true,
          maxAge: 60 * 60 * 24 * 7 * 4 * 3,
          path: "/",
          sameSite: true,
          secure: !IS_DEV,
        },
      });
    }

    return { identityToken, refreshToken };
  }
}
