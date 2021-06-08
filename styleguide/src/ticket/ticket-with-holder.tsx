import clsx from "clsx";
import React from "react";
import { Lanyard } from "./lanyard";
import { Ticket } from "./ticket";
import { TicketHolder } from "./ticket-holder";

type Props = {
  ticketSize: "medium";
};

export const TicketWithHolder = ({ ticketSize }: Props) => {
  return (
    <div
      className={clsx({
        "max-w-md": ticketSize === "medium",
      })}
    >
      <Lanyard />

      <TicketHolder>
        <Ticket name={"Test name"} />
      </TicketHolder>
    </div>
  );
};
