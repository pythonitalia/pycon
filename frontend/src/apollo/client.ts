import { ApolloClient, Operation } from "@apollo/client/core";
import merge from "deepmerge";
import { DefinitionNode } from "graphql";

import isEqual from "../helpers/lodash-is-equal";
import { createClient } from "./create-client";

export const APOLLO_STATE_PROP_NAME = "__APOLLO_STATE__";

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

let cachedClient: ApolloClient<any> | null = null;

export const getApolloClient = (initialState = null, serverCookies = null) => {
  const client =
    cachedClient ??
    createClient({
      serverCookies,
    });

  if (initialState) {
    const existingCache = client.extract();
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
    client.cache.restore(data);
  }

  if (typeof window === "undefined") {
    return client;
  }

  if (!cachedClient) {
    cachedClient = client;
  }
  return cachedClient;
};

export function addApolloState(client, pageProps, revalidate = 60 * 3) {
  if (pageProps?.props) {
    pageProps.props[APOLLO_STATE_PROP_NAME] = client.cache.extract();
  }

  const returnValue = {
    ...pageProps,
  };

  if (revalidate !== null) {
    returnValue.revalidate = revalidate;
  }

  return returnValue;
}
