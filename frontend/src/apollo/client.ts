import { navigate } from "@reach/router";
import {
  InMemoryCache,
  IntrospectionFragmentMatcher,
} from "apollo-cache-inmemory";
import { ApolloClient } from "apollo-client";
import { ApolloLink } from "apollo-link";
import { onError } from "apollo-link-error";
import { HttpLink } from "apollo-link-http";
import { GraphQLError } from "graphql";
import fetch from "isomorphic-fetch";

import { setLoginState } from "../app/profile/hooks";
import introspectionQueryResultData from "../generated/fragment-types.json";
const fragmentMatcher = new IntrospectionFragmentMatcher({
  introspectionQueryResultData,
});

const isUserLoggedOut = (graphErrors: readonly GraphQLError[]) =>
  !!graphErrors.find(e => e.message === "User not logged in");

const errorLink = onError(({ graphQLErrors, networkError }) => {
  if (graphQLErrors) {
    graphQLErrors.map(({ message, locations, path }) =>
      console.warn(
        `[GraphQL error]: Message: ${message}, Location: ${locations}, Path: ${path}`,
      ),
    );

    if (isUserLoggedOut(graphQLErrors)) {
      setLoginState(false);
      navigate("/en/login");
    }
  }

  if (networkError) {
    console.warn(`[Network error]: ${networkError}`);
  }
});

const httpLink = new HttpLink({
  uri: "/graphql",
  fetch,
});

const link = ApolloLink.from([errorLink, httpLink]);

const cache = new InMemoryCache({ fragmentMatcher });

export const client = new ApolloClient({
  link,
  cache,
});
