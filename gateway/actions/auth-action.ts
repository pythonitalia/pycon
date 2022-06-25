import { IS_DEV } from "../config";
import {
  createIdentityToken,
  createRefreshToken,
} from "../pastaporto/identity";
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

export class AuthActionPayload {
  constructor(readonly id: string, readonly jwtAuthId: number) {}
}

export class AuthAction extends PastaportoAction<
  Options,
  Return,
  AuthActionPayload
> {
  async apply(context: any) {
    const sub = `${this.payload.id}`;
    const identityToken = createIdentityToken(sub, this.payload.jwtAuthId);
    let refreshToken;

    context.res.cookie("identity", identityToken, {
      httpOnly: true,
      maxAge: SECONDS_IN_84_DAYS,
      path: "/",
      sameSite: "lax",
      secure: !IS_DEV,
    });

    if (!this.options?.identityOnly) {
      refreshToken = createRefreshToken(sub, this.payload.jwtAuthId);

      context.res.cookie("refreshIdentity", refreshToken, {
        httpOnly: true,
        maxAge: SECONDS_IN_84_DAYS,
        path: "/",
        sameSite: "lax",
        secure: !IS_DEV,
      });
    }

    return { identityToken, refreshToken };
  }
}
