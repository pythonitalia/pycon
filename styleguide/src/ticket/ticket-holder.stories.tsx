import React from "react";

import { TicketHolder } from "./ticket-holder";

export default {
  title: "Ticket holder",
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

export const Primary = () => (
  <TicketHolder>
    Ticket here Ticket here Ticket here Ticket here Ticket here Ticket here
  </TicketHolder>
);
