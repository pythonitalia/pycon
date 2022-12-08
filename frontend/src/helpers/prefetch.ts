import { ApolloClient } from "@apollo/client/core";

import { queryHeader } from "~/types";

export const prefetchSharedQueries = async (
  client: ApolloClient<any>,
  _language: string,
) => {
  const header = queryHeader(client, {
    code: process.env.conferenceCode,
  });

  return Promise.all([header]);
};
