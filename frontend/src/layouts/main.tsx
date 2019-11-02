import React from "react";
import styled from "styled-components";

import { Footer } from "../components/footer";
import { Header } from "../components/header";
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
      <Header />

      <Footer />
    </Wrapper>
  </LanguageContext.Provider>
);
