import React from "react";
import { TicketWithHolder } from "../ticket";
import { FullscreenOverlay } from "./fullscreen-overlay";

export default {
  title: "Fullscreen overlay",
  argTypes: {
    contents: {
      defaultValue: "ticket with holder",
      control: {
        type: "select",
        options: ["ticket with holder", "simple text"],
      },
    },
  },
};

export const Primary = ({ contents }) => {
  return (
    <FullscreenOverlay>
      {contents === "ticket with holder" && (
        <TicketWithHolder ticketSize="medium" />
      )}
      {contents === "simple text" && <span>your text here</span>}
    </FullscreenOverlay>
  );
};
