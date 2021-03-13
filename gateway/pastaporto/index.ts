import { AuthenticationError } from "apollo-server-errors";
import { TokenExpiredError } from "jsonwebtoken";
import { Pastaporto } from "./entities";

export const createPastaporto = async (token?: string): Promise<Pastaporto> => {
  if (!token) {
    // not authenticated
    return Pastaporto.unauthenticated();
  }

  try {
    return await Pastaporto.fromIdentityToken(token);
  } catch (e) {
    console.error("Unable to get pastaporto from identity", e);

    if (e instanceof TokenExpiredError) {
      throw new AuthenticationError(`Identity is not valid (expired token)`);
    } else {
      throw e;
    }
  }
};
