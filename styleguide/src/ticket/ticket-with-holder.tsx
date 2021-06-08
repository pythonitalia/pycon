import clsx from "clsx";
import React from "react";
import { Lanyard } from "./lanyard";
import { Ticket, TicketProps } from "./ticket";
import { TicketHolder } from "./ticket-holder";

type Props = {
  ticketSize: "medium";
  ticket: TicketProps;
};

export const TicketWithHolder = ({ ticketSize, ticket }: Props) => {
  return (
    <div
      className={clsx({
        "max-w-md": ticketSize === "medium",
      })}
    >
      <Lanyard />

      <TicketHolder>
        <Ticket {...ticket} />
      </TicketHolder>
    </div>
  );
};
