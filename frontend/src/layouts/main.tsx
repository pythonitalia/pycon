import React from "react";
import styled from "styled-components";

import { ErrorBoundary } from "../components/error-boundary";
import { Footer } from "../components/footer";
import { Topbar } from "../components/topbar";
import { LanguageContext } from "../context/language";

const Wrapper = styled.div`
  padding-top: 80px;
`;

export const MainLayout = (props: {
  children: React.ReactNode;
  language: string;
}) => (
  <LanguageContext.Provider value={props.language}>
    <Wrapper>
      <Topbar />
      <ErrorBoundary>{props.children}</ErrorBoundary>
      <Footer />
    </Wrapper>
  </LanguageContext.Provider>
);
