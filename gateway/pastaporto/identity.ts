import jwt from "jsonwebtoken";

import { ClearAuthAction } from "../actions/clear-auth-action";
import { IDENTITY_SECRET } from "../config";

export type DecodedIdentity = {
  sub: string;
  jwtAuthId: number;
};

export const decodeIdentity = (
  token: string,
  ignoreExpiration = false,
): DecodedIdentity => {
  return jwt.verify(token, IDENTITY_SECRET!, {
    issuer: "gateway",
    audience: "identity",
    algorithms: ["HS256"],
    ignoreExpiration,
  }) as DecodedIdentity;
};

export const createIdentityToken = (sub: string, jwtAuthId: number): string => {
  if (!sub) {
    throw new Error("Empty subject not allowed");
  }

  if (!jwtAuthId) {
    throw new Error("Empty jwtAuthId not allowed");
  }

  return jwt.sign(
    {
      jwtAuthId,
    },
    IDENTITY_SECRET!,
    {
      subject: sub,
      issuer: "gateway",
      expiresIn: "15m",
      audience: "identity",
      algorithm: "HS256",
    },
  );
};

export const decodeRefreshToken = (
  token: string,
  decodedIdentity: DecodedIdentity,
) => {
  return jwt.verify(token, IDENTITY_SECRET!, {
    subject: decodedIdentity.sub,
    issuer: "gateway",
    audience: "refresh",
    algorithms: ["HS256"],
  });
};

export const createRefreshToken = (sub: string, jwtAuthId: number): string => {
  if (!sub) {
    throw new Error("Empty subject not allowed");
  }

  return jwt.sign(
    {
      jwtAuthId,
    },
    IDENTITY_SECRET!,
    {
      subject: sub,
      issuer: "gateway",
      expiresIn: "84 days",
      audience: "refresh",
      algorithm: "HS256",
    },
  );
};

export const removeIdentityTokens = async (temporaryContext: object) => {
  console.log("Clearing identity tokens");

  // Clear the cookies if the jwt are not valid anymore
  const action = new ClearAuthAction();
  await action.apply(temporaryContext);
};
