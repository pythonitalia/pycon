import { ApolloLink, HttpLink } from "@apollo/client";
import { InMemoryCache } from "@apollo/client/cache";
import { ApolloClient } from "@apollo/client/core";
import { onError } from "@apollo/client/link/error";
import { GraphQLError } from "graphql";
import fetch from "isomorphic-fetch";

import { setLoginState } from "../app/profile/hooks";
import introspectionQueryResultData from "../generated/fragment-types.json";

const isUserLoggedOut = (graphErrors: readonly GraphQLError[]) =>
  !!graphErrors.find((e) => e.message === "User not logged in");

const errorLink = onError(({ graphQLErrors, networkError }) => {
  if (graphQLErrors) {
    graphQLErrors.map(({ message, locations, path }) =>
      console.warn(
        `[GraphQL error]: Message: ${message}, Location: ${locations}, Path: ${path}`,
      ),
    );

    if (isUserLoggedOut(graphQLErrors)) {
      setLoginState(false);

      // TODO: get current locale
      window.location.href = "/en/login";

      return;
    }
  }

  if (networkError) {
    console.warn(`[Network error]: ${networkError}`);
  }
});

const httpLink = new HttpLink({
  uri: process.browser ? "/graphql" : process.env.API_URL,
  fetch,
});

const link = ApolloLink.from([errorLink, httpLink]);

export const getApolloClient = ({ initialState }: any) =>
  new ApolloClient({
    link,
    cache: new InMemoryCache({
      possibleTypes: introspectionQueryResultData.possibleTypes,
    }).restore(initialState || {}),
  });
