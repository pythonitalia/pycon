import React from "react";

import { ThemeProvider } from "fannypack";
import styled from "styled-components";
import { Footer } from "../components/footer";
import { Topbar } from "../components/topbar";
import { theme } from "../config/theme";

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
