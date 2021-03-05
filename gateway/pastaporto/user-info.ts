import { SERVICE_TO_SERVICE_SECRET, USERS_SERVICE } from "../config";
import { GraphQLClient, gql } from "graphql-request";

const USERS_SERVICE_INTERNAL_API_ENDPOINT = `${USERS_SERVICE}/internal-api`;

export type User = {
  id: number;
  email: string;
  isStaff: boolean;
};

export const fetchUserInfo = async (id: number): Promise<User> => {
  const client = new GraphQLClient(USERS_SERVICE_INTERNAL_API_ENDPOINT, {
    headers: {
      "x-service-key": SERVICE_TO_SERVICE_SECRET as string,
    },
  });

  const query = gql`
    query($id: ID) {
      user(id: $id) {
        id
        email
        isStaff
      }
    }
  `;

  const data = await client.request(query, { id });
  return data.user as User;
};
