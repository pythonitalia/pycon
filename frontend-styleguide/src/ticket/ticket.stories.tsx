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
    company: {
      defaultValue: "Made.com",
      control: {
        type: "text",
      },
    },
    username: {
      defaultValue: "@etty",
      control: {
        type: "text",
      },
    },
  },
  parameters: {
    layout: "centered",
    backgrounds: {
      default: "default",
      values: [
        {
          name: "default",
          value: "#e0e0e0",
        },
      ],
    },
  },
};

export const Primary = (props) => (
  <div className="max-w-2xl">
    <Ticket {...props} />
  </div>
);
