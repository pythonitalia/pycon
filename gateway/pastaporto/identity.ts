import { IDENTITY_SECRET } from "../config";
import jwt from "jsonwebtoken";
import { ClearAuthAction } from "../actions/clear-auth-action";

type DecodedIdentity = {
  sub: string;
};

export const decodeIdentity = (
  token: string,
  ignoreExpiration: boolean = false,
): DecodedIdentity => {
  return jwt.verify(token, IDENTITY_SECRET!, {
    issuer: "gateway",
    audience: "identity",
    algorithms: ["HS256"],
    ignoreExpiration,
  }) as DecodedIdentity;
};

export const createIdentityToken = (sub: string): string => {
  if (!sub) {
    throw new Error("Empty subject not allowed");
  }

  return jwt.sign({}, IDENTITY_SECRET!, {
    subject: sub,
    issuer: "gateway",
    expiresIn: "15m",
    audience: "identity",
    algorithm: "HS256",
    notBefore: 0,
  });
};

export const decodeRefreshToken = (token: string, sub: string) => {
  return jwt.verify(token, IDENTITY_SECRET!, {
    subject: sub,
    issuer: "gateway",
    audience: "refresh",
    algorithms: ["HS256"],
  });
};

export const createRefreshToken = (sub: string): string => {
  if (!sub) {
    throw new Error("Empty subject not allowed");
  }

  return jwt.sign({}, IDENTITY_SECRET!, {
    subject: sub,
    issuer: "gateway",
    expiresIn: "84 days",
    audience: "refresh",
    algorithm: "HS256",
    notBefore: 0,
  });
};

export const removeIdentityTokens = async (temporaryContext: object) => {
  console.log("Clearing identity tokens");

  // Clear the cookies if the jwt are not valid anymore
  const action = new ClearAuthAction({});
  await action.apply(temporaryContext);
};
