import React from "react";
import { Header } from "./header";

export default {
  title: "Header",
};

export const Standard = () => (
  <Header
    links={[
      {
        href: "/",
        title: "Home",
      },
      {
        href: "/",
        title: "Schedule",
      },
    ]}
  />
);
