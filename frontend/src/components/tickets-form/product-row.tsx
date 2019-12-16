/** @jsx jsx */
import { Box, Grid, Text } from "@theme-ui/components";
import { jsx } from "theme-ui";

import { AddProductWithVariation } from "./add-product-with-variation";
import { AddRemoveProduct } from "./add-remove-product";
import { Ticket } from "./types";

type ProductRowProps = {
  ticket: Ticket;
  quantity: number;
  addProduct: (ticketId: string, variation?: string) => void;
  removeProduct: (ticketId: string) => void;
};

export const ProductRow: React.SFC<ProductRowProps> = ({
  ticket,
  quantity,
  addProduct,
  removeProduct,
}) => {
  const hasVariation = ticket.variations && ticket.variations.length > 0;

  return (
    <Box sx={{ mb: 4 }}>
      <Grid
        sx={{
          gridTemplateColumns: ["1fr", "1fr 180px"],
        }}
      >
        <Box>
          <Text as="label" variant="label">
            {ticket.name}
          </Text>

          <Text>
            Price:{" "}
            <Text as="span" sx={{ fontWeight: "bold" }}>
              {ticket.defaultPrice} EUR
            </Text>
          </Text>

          <Text>{ticket.description}</Text>
        </Box>

        {!hasVariation && (
          <AddRemoveProduct
            quantity={quantity}
            increase={() => addProduct(ticket.id)}
            decrease={() => removeProduct(ticket.id)}
          />
        )}

        {hasVariation && (
          <AddProductWithVariation
            addVariation={(variation: string) =>
              addProduct(ticket.id, variation)
            }
            ticket={ticket}
          />
        )}
      </Grid>
    </Box>
  );
};
