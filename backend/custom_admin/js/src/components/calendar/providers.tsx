import { ApolloClient, InMemoryCache, ApolloProvider } from "@apollo/client";
import React from "react";
import { DndProvider } from "react-dnd";
import { HTML5Backend } from "react-dnd-html5-backend";

import { Calendar } from ".";
import { getVars } from "./vars";

const APOLLO_CLIENT_URL =
  getVars().apolloGraphQLUrl || "http://localhost:4000/graphql";

const client = new ApolloClient({
  uri: APOLLO_CLIENT_URL,
  cache: new InMemoryCache(),
});

export const Providers = () => {
  console.log("!!", client);
  return (
    <ApolloProvider client={client}>
      <DndProvider backend={HTML5Backend}>
        <Calendar />
      </DndProvider>
    </ApolloProvider>
  );
};
