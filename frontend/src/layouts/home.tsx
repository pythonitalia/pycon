import React from "react";

import { ThemeProvider } from "fannypack";
import { Topbar } from "../components/topbar";
import { theme } from "../config/theme";
import { Footer } from "../components/footer";
import styled from "styled-components";

const Wrapper = styled.div`
  padding-top: 80px;
`;

export const HomeLayout = (props: { children: React.ReactNode }) => {
  return (
    <ThemeProvider theme={theme}>
      <Wrapper>
        <Topbar />
        <div>{props.children}</div>
        <Footer />
      </Wrapper>
    </ThemeProvider>
  );
};
