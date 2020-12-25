import { ApolloLink, HttpLink } from "@apollo/client";
import { InMemoryCache } from "@apollo/client/cache";
import { ApolloClient, Operation } from "@apollo/client/core";
import { onError } from "@apollo/client/link/error";
import * as Sentry from "@sentry/node";
import { DefinitionNode, GraphQLError } from "graphql";
import { print } from "graphql/language/printer";
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

    if (isUserLoggedOut(graphQLErrors) && typeof window !== "undefined") {
      // If we are not in SSR, reset the login state of the user
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

type ApolloQueryDefinition = DefinitionNode & {
  operation?: string;
};

export const getQueryType = (operation: Operation): string | undefined => {
  const definitions = operation.query.definitions as ApolloQueryDefinition[];
  const queryType = definitions.find((definition) =>
    Boolean(definition.operation),
  )?.operation;
  return queryType;
};

const sentryLink = new ApolloLink((operation, forward) => {
  Sentry.addBreadcrumb({
    category: "graphql",
    data: {
      type: getQueryType(operation),
      name: operation.operationName,
      query: print(operation.query),
      variables: operation.variables,
    },
    level: Sentry.Severity.Debug,
  });

  return forward(operation);
});

const link = ApolloLink.from([sentryLink, errorLink, httpLink]);

export const getApolloClient = ({ initialState }: any) =>
  new ApolloClient({
    link,
    cache: new InMemoryCache({
      possibleTypes: introspectionQueryResultData.possibleTypes,
    }).restore(initialState || {}),
  });
