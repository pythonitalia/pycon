import {
  InMemoryCache,
  IntrospectionFragmentMatcher,
} from "apollo-cache-inmemory";
import { ApolloClient } from "apollo-client";
import { HttpLink } from "apollo-link-http";
import fetch from "isomorphic-fetch";

import introspectionQueryResultData from "../generated/fragment-types.json";
const fragmentMatcher = new IntrospectionFragmentMatcher({
  introspectionQueryResultData,
});

const link = new HttpLink({
  uri: "/graphql",
  fetch,
});

const cache = new InMemoryCache({ fragmentMatcher });

export const client = new ApolloClient({
  link,
  cache,
});
