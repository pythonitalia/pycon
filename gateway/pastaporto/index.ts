import { AuthAction } from "../actions/auth-action";
import { AuthenticationError } from "apollo-server-errors";
import { TokenExpiredError } from "jsonwebtoken";
import { Pastaporto } from "./entities";
import { decodeIdentity, decodeRefreshToken } from "./identity";

export const createPastaporto = async (
  token: string | null,
  temporaryContext: object,
  refreshToken: string | null = null,
): Promise<Pastaporto> => {
  if (!token) {
    // not authenticated
    return Pastaporto.unauthenticated();
  }

  try {
    return await Pastaporto.fromIdentityToken(token);
  } catch (e) {
    if (e instanceof TokenExpiredError) {
      if (!refreshToken) {
        console.log(
          "Expired identity, refresh token is missing or refresh flow failed",
        );
        throw new AuthenticationError(`Identity is not valid (expired token)`);
      }

      console.log("Expired identity, trying to refresh token");

      const subject = decodeIdentity(token, true).sub;

      if (subject && canRefreshIdentity(refreshToken, subject)) {
        const newIdentity = await createNewIdentity(subject, temporaryContext);
        return createPastaporto(newIdentity, temporaryContext);
      } else {
        throw new AuthenticationError(`Identity is not valid (expired token)`);
      }
    } else {
      console.error("Unable to get pastaporto from identity", e);
      throw e;
    }
  }
};

export const canRefreshIdentity = (refreshToken: string, subject: string) => {
  try {
    decodeRefreshToken(refreshToken, subject);
    console.info(`Refresh token for user ${subject} accepted`);
    return true;
  } catch (e) {
    console.info("Cannot refresh token:", e);
    return false;
  }
};

const createNewIdentity = async (sub: string, temporaryContext: object) => {
  // Create a new refreshed identity for the user
  // We use the AuthAction sending the temporary context object
  // so we can re-use the existing cookies flow
  const action = new AuthAction({ id: sub }, { identityOnly: true });
  const { identityToken } = await action.apply(temporaryContext);
  console.log(
    `created new identity for user-id ${sub} using refresh token flow`,
  );
  return identityToken as string;
};
