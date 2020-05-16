/** @jsx jsx */
import React from "react";
import { Box, jsx } from "theme-ui";

import { SelectedProducts } from "../tickets-page/types";
import { ProductRow } from "./product-row";
import { SelectedProductsWithVariationsList } from "./selected-products-with-variation-list";
import { Ticket } from "./types";

type Props = {
  isBusiness: boolean;
  tickets: Ticket[];
  selectedProducts: SelectedProducts;
  addProduct: (id: string, variant?: string) => void;
  removeProduct: (id: string, variant?: string) => void;
};

export const TicketsForm: React.SFC<Props> = ({
  isBusiness,
  tickets,
  selectedProducts,
  addProduct,
  removeProduct,
}) => {
  const ticketsToShow = tickets.filter((ticket) => {
    if (ticket.variations!.length > 0) {
      return true;
    }

    if (isBusiness && ticket.name.toLowerCase().includes("business")) {
      return true;
    }

    if (!isBusiness && !ticket.name.toLowerCase().includes("business")) {
      return true;
    }

    return false;
  });

  return (
    <React.Fragment>
      {ticketsToShow.map((ticket) => (
        <Box key={ticket.id}>
          <ProductRow
            quantity={selectedProducts[ticket.id]?.length ?? 0}
            ticket={ticket}
            addProduct={addProduct}
            removeProduct={removeProduct}
          />
        </Box>
      ))}

      <SelectedProductsWithVariationsList
        selectedProducts={selectedProducts}
        products={tickets}
        removeProduct={removeProduct}
      />
    </React.Fragment>
  );
};
