import React from "react";
import { Ticket } from "./ticket";

export default {
  title: "Ticket",
  argTypes: {
    name: {
      defaultValue: "Ester Beltrami",
      control: {
        type: "text",
      },
    },
  },
};

export const Primary = (props) => (
  <div className="max-w-2xl">
    <Ticket {...props} />
  </div>
);
