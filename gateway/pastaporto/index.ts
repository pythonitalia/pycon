import { AuthenticationError } from "apollo-server-errors";
import { TokenExpiredError } from "jsonwebtoken";

import { AuthAction, AuthActionPayload } from "../actions/auth-action";
import { ApolloContext } from "../context";
import { Pastaporto } from "./entities";
import {
  DecodedIdentity,
  decodeIdentity,
  decodeRefreshToken,
  removeIdentityTokens,
} from "./identity";

export const createPastaporto = async (
  token: string | null,
  temporaryContext: ApolloContext,
  refreshToken: string | null = null,
): Promise<Pastaporto> => {
  if (!token) {
    console.info("creating pastaporto: no token passed, not authenticated");
    // not authenticated
    return Pastaporto.unauthenticated();
  }

  try {
    return await Pastaporto.fromIdentityToken(token);
  } catch (e) {
    if (e instanceof TokenExpiredError) {
      if (!refreshToken) {
        console.info(
          "Expired identity, refresh token is missing or refresh flow failed",
        );
        throw new AuthenticationError(`Identity is not valid (expired token)`);
      }

      console.info("Expired identity, trying to refresh token");

      const decodedIdentity = decodeIdentity(token, true);

      if (
        decodedIdentity &&
        canRefreshIdentity(refreshToken, decodedIdentity)
      ) {
        const newIdentity = await createNewIdentity(
          decodedIdentity,
          temporaryContext,
        );
        return createPastaporto(newIdentity, temporaryContext);
      } else {
        throw new AuthenticationError(`Identity is not valid (expired token)`);
      }
    } else {
      console.error("Unable to get pastaporto from identity", e);
      removeIdentityTokens(temporaryContext);
      throw e;
    }
  }
};

export const canRefreshIdentity = (
  refreshToken: string,
  decodedIdentity: DecodedIdentity,
) => {
  try {
    decodeRefreshToken(refreshToken, decodedIdentity);
    console.info(`Refresh token for user ${decodedIdentity.sub} accepted`);
    return true;
  } catch (e) {
    console.info("Cannot refresh token:", e);
    return false;
  }
};

const createNewIdentity = async (
  decodedIdentity: DecodedIdentity,
  temporaryContext: ApolloContext,
) => {
  // Create a new refreshed identity for the user
  // We use the AuthAction sending the temporary context object
  // so we can re-use the existing cookies flow
  const action = new AuthAction(
    new AuthActionPayload(decodedIdentity.sub, decodedIdentity.jwtAuthId),
    {
      identityOnly: true,
    },
  );
  const { identityToken } = await action.apply(temporaryContext);
  console.info(
    `created new identity for user-id ${decodedIdentity.sub} using refresh token flow`,
  );
  return identityToken as string;
};
