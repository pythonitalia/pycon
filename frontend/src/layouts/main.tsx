import { ApolloProvider } from "@apollo/react-hooks";
import {
  InMemoryCache,
  IntrospectionFragmentMatcher,
} from "apollo-cache-inmemory";
import { ApolloClient } from "apollo-client";
import { HttpLink } from "apollo-link-http";
import { ThemeProvider } from "fannypack";
import React from "react";
import styled from "styled-components";

import { Footer } from "../components/footer";
import { Topbar } from "../components/topbar";
import { theme } from "../config/theme";
import { LanguageContext } from "../context/language";
import introspectionQueryResultData from "../generated/fragment-types.json";

const fragmentMatcher = new IntrospectionFragmentMatcher({
  introspectionQueryResultData,
});

const Wrapper = styled.div`
  padding-top: 80px;
`;

const link = new HttpLink({
  uri: "/graphql",
});

const cache = new InMemoryCache({ fragmentMatcher });

const client = new ApolloClient({
  link,
  cache,
});

export const MainLayout = (props: {
  children: React.ReactNode;
  language: string;
}) => (
  <ApolloProvider client={client}>
    <LanguageContext.Provider value={props.language}>
      <ThemeProvider theme={theme}>
        <Wrapper>
          <Topbar />
          {props.children}
          <Footer />
        </Wrapper>
      </ThemeProvider>
    </LanguageContext.Provider>
  </ApolloProvider>
);
