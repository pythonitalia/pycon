import React from "react";
import { Marquee } from "./marquee";

export default {
  title: "Marquee",
  argTypes: {
    text: {
      defaultValue: "Hello there 👋",
      control: {
        type: "text",
      },
    },
    speed: {
      defaultValue: "medium",
      control: {
        type: "select",
        options: ["slow", "medium"],
      },
    },
  },
};

export const Standard = ({ text, ...props }) => (
  <Marquee {...props}>{text}</Marquee>
);
