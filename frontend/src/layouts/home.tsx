import React from "react";
import { Topbar } from "../components/topbar";
import { ThemeProvider } from "fannypack";
import { theme } from "../config/theme";

export const HomeLayout = (props: { children: React.ReactNode }) => {
  return (
    <ThemeProvider theme={theme}>
      <Topbar />
      <div>{props.children}</div>
    </ThemeProvider>
  );
};
