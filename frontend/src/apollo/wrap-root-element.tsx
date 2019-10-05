import { ApolloProvider } from "@apollo/react-hooks";
import React from "react";

import { client } from "./client";

export const wrapRootElement = ({ element }: { element: any }) => (
  <ApolloProvider client={client}>{element}</ApolloProvider>
);
