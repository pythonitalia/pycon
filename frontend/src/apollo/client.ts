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

const errorLink = onError(({ graphQLErrors, networkError }) => {
  if (graphQLErrors) {
    graphQLErrors.map(({ message, locations, path }) =>
      console.warn(
        `[GraphQL error]: Message: ${message}, Location: ${locations}, Path: ${path}`,
      ),
    );
  }

  if (networkError) {
    console.warn(`[Network error]: ${networkError}`);
  }
  if (networkError && networkError.statusCode === 401){
    // TODO logout()
  }
});

const httpLink = new HttpLink({
  uri: "/graphql",
  fetch,
});

const link = ApolloLink.from([
  errorLink,
  httpLink,
]);

const cache = new InMemoryCache({ fragmentMatcher });

export const client = new ApolloClient({
  link,
  cache,
});
