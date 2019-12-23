/** @jsx jsx */
import { Box } from "@theme-ui/components";
import React from "react";
import { jsx } from "theme-ui";

import { SelectedProducts } from "../tickets-page/types";
import { ProductRow } from "./product-row";
import { SelectedProductsWithVariationsList } from "./selected-products-with-variation-list";
import { Ticket } from "./types";

type Props = {
  tickets: Ticket[];
  selectedProducts: SelectedProducts;
  addProduct: (id: string, variant?: string) => void;
  removeProduct: (id: string, variant?: string) => void;
};

export const TicketsForm: React.SFC<Props> = ({
  tickets,
  selectedProducts,
  addProduct,
  removeProduct,
}) => (
  <React.Fragment>
    {tickets.map(ticket => (
      <Box key={ticket.id}>
        <ProductRow
          quantity={
            selectedProducts[ticket.id] ? selectedProducts[ticket.id].length : 0
          }
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
