import clsx from "clsx";
import React from "react";
import { Lanyard } from "./lanyard";
import { Ticket, TicketProps } from "./ticket";
import { TicketHolder } from "./ticket-holder";

type Props = {
  ticketSize: "medium";
  ticket: TicketProps;
  ticketHolderRef?: React.Ref<HTMLDivElement>;
};

export const TicketWithHolder = ({
  ticketSize,
  ticket,
  ticketHolderRef,
}: Props) => {
  return (
    <div
      className={clsx("w-full px-4 sm:px-0", {
        "max-w-md": ticketSize === "medium",
      })}
    >
      <Lanyard />

      <TicketHolder ref={ticketHolderRef}>
        <Ticket {...ticket} />
      </TicketHolder>
    </div>
  );
};
