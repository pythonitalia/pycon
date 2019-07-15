import React from "react";

import { ThemeProvider } from "fannypack";
import { Topbar } from "../components/topbar";
import { theme } from "../config/theme";

export const HomeLayout = (props: { children: React.ReactNode }) => {
  return (
    <ThemeProvider theme={theme}>
      <Topbar />
      <div>{props.children}</div>
    </ThemeProvider>
  );
};
