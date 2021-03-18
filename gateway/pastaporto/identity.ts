import { IDENTITY_SECRET } from "../config";
import jwt from "jsonwebtoken";
import { promisify } from "util";
import { ClearAuthAction } from "../actions/clear-auth-action";

const jwtVerify = promisify(jwt.verify);
const jwtSign = promisify(jwt.sign);

type DecodedIdentity = {
  sub: string;
};

export const decodeIdentity = async (
  token: string,
  ignoreExpiration: boolean = false,
): Promise<DecodedIdentity> => {
  return jwtVerify(token, IDENTITY_SECRET, {
    issuer: "gateway",
    audience: "identity",
    algorithms: ["HS256"],
    ignoreExpiration,
  });
};

export const createIdentityToken = async (sub: string): Promise<string> => {
  return jwtSign({}, IDENTITY_SECRET, {
    subject: sub,
    issuer: "gateway",
    expiresIn: "15m",
    audience: "identity",
    algorithm: "HS256",
  });
};

export const decodeRefreshToken = (token: string, sub: string) => {
  return jwtVerify(token, IDENTITY_SECRET, {
    subject: sub,
    issuer: "gateway",
    audience: "refresh",
    algorithms: ["HS256"],
  });
};

export const createRefreshToken = async (sub: string): Promise<string> => {
  return jwtSign({}, IDENTITY_SECRET, {
    subject: sub,
    issuer: "gateway",
    expiresIn: "84 days",
    audience: "refresh",
    algorithm: "HS256",
  });
};

export const removeIdentityTokens = async (temporaryContext: object) => {
  console.log("Clearing identity tokens");

  // Clear the cookies if the jwt are not valid anymore
  const action = new ClearAuthAction({});
  await action.apply(temporaryContext);
};
