/** @jsx jsx */
import { Box, Button, Flex, Grid } from "@theme-ui/components";
import React from "react";
import { jsx } from "theme-ui";

import { Ticket } from "./types";

export const SelectedProductsWithVariationsList: React.SFC<{
  products: Ticket[];
  selectedProducts: {
    [id: string]: {
      id: string;
      variation?: string;
      quantity: number;
    };
  };
  removeProduct: (id: string, variation: string) => void;
}> = ({ products, selectedProducts, removeProduct }) => {
  const productsToShow = Object.values(selectedProducts).filter(
    product => product.quantity > 0 && product.variation,
  );

  const productsById = Object.fromEntries(
    products.map(product => [product.id, product]),
  );

  return (
    <React.Fragment>
      {productsToShow.map(selectedProduct => {
        const product = productsById[selectedProduct.id];
        return (
          <Grid
            sx={{ gridTemplateColumns: "1fr 50px", my: 3 }}
            key={`${selectedProduct.id}${selectedProduct.variation}`}
          >
            <Flex sx={{ display: "flex", alignItems: "center" }}>
              <Box>
                <strong>{selectedProduct.quantity}x</strong> {product.name}{" "}
                <strong>
                  (
                  {
                    product.variations?.find(
                      variation => variation.id === selectedProduct.variation,
                    )?.value
                  }
                  )
                </strong>
              </Box>
            </Flex>
            <Button
              variant="minus"
              onClick={() =>
                removeProduct(selectedProduct.id, selectedProduct.variation!)
              }
            >
              -
            </Button>
          </Grid>
        );
      })}
    </React.Fragment>
  );
};
