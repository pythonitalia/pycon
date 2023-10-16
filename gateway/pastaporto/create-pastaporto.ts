import { gql, GraphQLClient } from "graphql-request";
import jwt from "jsonwebtoken";

import { SERVICE_TO_SERVICE_SECRET, USERS_SERVICE } from "../config";

const USERS_SERVICE_INTERNAL_API_ENDPOINT = `${USERS_SERVICE}/internal-api`;

export const createPastaporto = async (
  identityToken: string | null,
): Promise<string | null> => {
  if (!identityToken) {
    return null;
  }

  const token: string = jwt.sign({}, SERVICE_TO_SERVICE_SECRET!, {
    issuer: "gateway",
    audience: "users-backend",
    expiresIn: "1m",
  });

  const client = new GraphQLClient(USERS_SERVICE_INTERNAL_API_ENDPOINT, {
    headers: {
      "x-service-token": token,
    },
  });

  const query = gql`
    query ($identityToken: String) {
      createPastaporto(identityToken: $identityToken) {
        pastaportoToken
      }
    }
  `;

  const data = await client.request(query, { identityToken });
  // @ts-ignore
  return data.createPastaporto.pastaportoToken;
};
