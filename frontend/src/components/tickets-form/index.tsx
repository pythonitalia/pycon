/** @jsxRuntime classic */

/** @jsx jsx */
import React from "react";
import { Box, jsx } from "theme-ui";

import { SelectedProducts } from "../tickets-page/types";
import { ProductRow } from "./product-row";
import { Ticket } from "./types";

type Props = {
  isBusiness: boolean;
  tickets: Ticket[];
  selectedProducts: SelectedProducts;
  addProduct: (id: string, variant?: string) => void;
  removeProduct: (id: string, variant?: string) => void;
};

export const TicketsForm = ({
  isBusiness,
  tickets,
  selectedProducts,
  addProduct,
  removeProduct,
}: Props) => {
  const ticketsToShow = tickets.filter((ticket) => {
    if (ticket.variations!.length > 0) {
      return true;
    }

    if (isBusiness && ticket.type === "BUSINESS") {
      return true;
    }

    if (!isBusiness && ticket.type !== "BUSINESS") {
      return true;
    }

    return false;
  });

  const ticketsByCategory = ticketsToShow.reduce((acc, ticket) => {
    const category = ticket.category;
    if (!acc[category]) {
      acc[category] = [];
    }
    acc[category].push(ticket);
    return acc;
  }, {} as { [category: string]: Ticket[] });

  return (
    <React.Fragment>
      {Object.entries(ticketsByCategory).map(([category, categoryTickets]) => (
        <Box key={category} sx={{ borderBottom: "primary" }}>
          <Box sx={{ maxWidth: "container", mx: "auto", px: 3 }}>
            {categoryTickets.map((ticket) => (
              <ProductRow
                key={ticket.id}
                quantity={selectedProducts[ticket.id]?.length ?? 0}
                ticket={ticket}
                addProduct={addProduct}
                removeProduct={removeProduct}
                selectedProducts={selectedProducts}
              />
            ))}
          </Box>
        </Box>
      ))}
    </React.Fragment>
  );
};
