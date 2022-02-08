import { ApolloClient } from "@apollo/client/core";

import { queryFooter, queryHeader, queryTopics } from "~/types";

export const prefetchSharedQueries = async (
  client: ApolloClient<any>,
  _language: string,
) => {
  const header = queryHeader(client, {
    code: process.env.conferenceCode,
  });

  const footer = queryFooter(client, {
    code: process.env.conferenceCode,
  });

  return Promise.all([header, footer]);
};
