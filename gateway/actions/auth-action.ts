import {
  createIdentityToken,
  createRefreshToken,
} from "../pastaporto/identity";
import { IS_DEV } from "../config";
import { PastaportoAction } from "./entities";

type Options = {
  identityOnly?: boolean;
};

type Return = {
  identityToken: string;
  refreshToken?: string;
};

const SECONDS_IN_1_HOUR = 60 * 60;
const SECONDS_IN_1_DAY = SECONDS_IN_1_HOUR * 24;
const SECONDS_IN_1_WEEK = SECONDS_IN_1_DAY * 7;

const SECONDS_IN_84_DAYS = SECONDS_IN_1_WEEK * 4 * 3;

export class AuthAction extends PastaportoAction<Options, Return> {
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
        maxAge: SECONDS_IN_84_DAYS,
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
          maxAge: SECONDS_IN_84_DAYS,
          path: "/",
          sameSite: true,
          secure: !IS_DEV,
        },
      });
    }

    return { identityToken, refreshToken };
  }
}
