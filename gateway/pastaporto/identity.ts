import { IDENTITY_SECRET } from "../config";
import jwt from "jsonwebtoken";
import { promisify } from "util";

const jwtVerify = promisify(jwt.verify);
const jwtSign = promisify(jwt.sign);

type DecodedIdentity = {
  sub: number;
};

export const decodeIdentity = async (
  token: string,
): Promise<DecodedIdentity> => {
  return jwtVerify(
    token,
    // @ts-ignore
    IDENTITY_SECRET,
  );
};

export const createIdentityToken = async (sub: number): Promise<string> => {
  return jwtSign({ sub }, IDENTITY_SECRET, { expiresIn: "15m" });
};
