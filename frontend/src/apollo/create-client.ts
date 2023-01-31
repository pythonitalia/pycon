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

const httpLink = new HttpLink({
  uri:
    typeof window === "undefined"
      ? process.env.API_URL_SERVER
      : process.env.API_URL,
  fetch,
  credentials: "include",
});

const link = ApolloLink.from([errorLink, httpLink]);

export const createClient = () => {
  return new ApolloClient({
    ssrMode: typeof window === "undefined",
    link,
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
