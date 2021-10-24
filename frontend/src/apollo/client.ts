import { ApolloLink, HttpLink } from "@apollo/client";
import { InMemoryCache } from "@apollo/client/cache";
import { ApolloClient, Operation } from "@apollo/client/core";
import { onError } from "@apollo/client/link/error";
import merge from "deepmerge";
import { DefinitionNode, GraphQLError } from "graphql";
import fetch from "isomorphic-fetch";
import isEqual from "lodash/isEqual";

import { setLoginState } from "../components/profile/hooks";
import introspectionQueryResultData from "../generated/fragment-types.json";

export const APOLLO_STATE_PROP_NAME = "__APOLLO_STATE__";

const isUserLoggedOut = (graphErrors: readonly GraphQLError[]) =>
  !!graphErrors.find(
    (e) =>
      e.message === "User not logged in" || e.message === "Not authenticated",
  );

const errorLink = onError(({ graphQLErrors, networkError, operation }) => {
  if (graphQLErrors) {
    graphQLErrors.map(({ message, locations, path }) =>
      console.warn(
        `[GraphQL error - ${operation.operationName}]: Message: ${message}, Location: ${locations}, Path: ${path}`,
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
    console.warn(
      `[Network error - ${operation.operationName}]: ${networkError}`,
    );
  }
});

const httpLink = new HttpLink({
  uri:
    typeof window === "undefined"
      ? process.env.API_URL_SERVER
      : process.env.API_URL,
  fetch,
  credentials: "include",
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

const link = ApolloLink.from([errorLink, httpLink]);

let cachedClient: ApolloClient<any> | null = null;

export const getApolloClient = (initialState = null) => {
  if (cachedClient === null) {
    cachedClient = new ApolloClient({
      ssrMode: typeof window === "undefined",
      link,
      cache: new InMemoryCache({
        possibleTypes: introspectionQueryResultData.possibleTypes,
      }),
    });
  }

  if (initialState) {
    const existingCache = cachedClient.extract();
    const data = merge(initialState, existingCache, {
      // combine arrays using object equality (like in sets)
      arrayMerge: (destinationArray, sourceArray) => [
        ...sourceArray,
        ...destinationArray.filter((d) =>
          sourceArray.every((s) => !isEqual(d, s)),
        ),
      ],
    });

    // Restore the cache with the merged data
    cachedClient.cache.restore(data);
  }

  return cachedClient;
};

export function addApolloState(pageProps) {
  if (pageProps?.props) {
    pageProps.props[APOLLO_STATE_PROP_NAME] = getApolloClient().cache.extract();
  }

  return pageProps;
}
