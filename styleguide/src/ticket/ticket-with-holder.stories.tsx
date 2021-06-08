import React from "react";

import { TicketWithHolder } from "./ticket-with-holder";

export default {
  title: "Ticket with holder",
  argTypes: {
    ticketSize: {
      defaultValue: "medium",
      control: {
        type: "radio",
        options: ["medium"],
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

export const Primary = (props) => <TicketWithHolder {...props} />;
