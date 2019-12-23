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
    }[];
  };
  removeProduct: (id: string, variation: string) => void;
}> = ({ products, selectedProducts, removeProduct }) => {
  const productsToShow = Object.values(selectedProducts).filter(
    p => p.length > 0 && p[0].variation,
  );

  const productsById = Object.fromEntries(
    products.map(product => [product.id, product]),
  );

  return (
    <React.Fragment>
      {productsToShow.map(selectedProduct => {
        const firstProduct = selectedProduct[0];
        const product = productsById[firstProduct.id];
        return (
          <Grid
            sx={{ gridTemplateColumns: "1fr 50px", my: 3 }}
            key={`${firstProduct.id}${firstProduct.variation}`}
          >
            <Flex sx={{ display: "flex", alignItems: "center" }}>
              <Box>
                <strong>{selectedProduct.length}x</strong> {product.name}{" "}
                <strong>
                  (
                  {
                    product.variations?.find(
                      variation => variation.id === firstProduct.variation,
                    )?.value
                  }
                  )
                </strong>
              </Box>
            </Flex>
            <Button
              variant="minus"
              onClick={() =>
                removeProduct(firstProduct.id, firstProduct.variation!)
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
