import React from "react";
import { Lanyard } from "./lanyard";
import { Ticket } from "./ticket";
import { TicketHolder } from "./ticket-holder";

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

export const Together = (props) => (
  <div className="max-w-md">
    <Lanyard />

    <TicketHolder>
      <Ticket {...props} />
    </TicketHolder>
  </div>
);
