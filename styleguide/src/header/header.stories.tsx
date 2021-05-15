import React from "react";
import { Header } from "./header";

export const Standard = (props) => (
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
    {...props}
  />
);

export default {
  title: "Header",
  component: Standard,
  argTypes: {
    backgroundColor: {
      control: {
        type: "radio",
        options: [
          "white",
          "black",
          "orange",
          "keppel",
          "casablanca",
          "aquamarine",
          "pink",
          "purple",
        ],
      },
    },
  },
};
