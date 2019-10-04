import { ThemeProvider } from "fannypack";
import React from "react";
import styled from "styled-components";

import { Footer } from "../components/footer";
import { Topbar } from "../components/topbar";
import { theme } from "../config/theme";
import { LanguageContext } from "../context/language";

const Wrapper = styled.div`
  padding-top: 80px;
`;

export const MainLayout = (props: {
  children: React.ReactNode;
  language: string;
}) => (
  <LanguageContext.Provider value={props.language}>
    <ThemeProvider theme={theme}>
      <Wrapper>
        <Topbar />
        {props.children}
        <Footer />
      </Wrapper>
    </ThemeProvider>
  </LanguageContext.Provider>
);
