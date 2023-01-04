import {
  HttpLink,
  ApolloClient,
  ApolloLink,
  InMemoryCache,
} from "@apollo/client";
import { onError } from "@apollo/client/link/error";
import { GraphQLError } from "graphql";

import { setLoginState } from "../components/profile/hooks";
import introspectionQueryResultData from "../generated/fragment-types.json";

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

const createHttpLink = (serverCookies: Record<string, string>) => {
  const isServer = typeof window === "undefined";
  const cookieHeader = isServer
    ? {
        cookie:
          serverCookies !== null
            ? Object.entries(serverCookies)
                .map(([key, value]) => `${key}=${value}`)
                .join("; ")
            : "",
      }
    : {};

  return new HttpLink({
    uri: isServer ? process.env.API_URL_SERVER : process.env.API_URL,
    fetch: (input, init) => {
      return fetch(input, {
        ...init,
        headers: {
          ...init?.headers,
          ...cookieHeader,
        },
      });
    },
    credentials: "include",
  });
};

export const createClient = ({ serverCookies = null } = {}) => {
  return new ApolloClient({
    ssrMode: typeof window === "undefined",
    link: ApolloLink.from([errorLink, createHttpLink(serverCookies)]),
    cache: new InMemoryCache({
      possibleTypes: introspectionQueryResultData.possibleTypes,
      typePolicies: {
        Day: {
          keyFields: ["day"],
        },
        SponsorsByLevel: {
          keyFields: ["level"],
        },
        TicketItem: {
          keyFields: ["id", "language"],
        },
      },
    }),
  });
};
