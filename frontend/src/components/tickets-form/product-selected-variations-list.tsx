/** @jsxRuntime classic */

/** @jsx jsx */
import React from "react";
import { Box, Flex, Grid, jsx } from "theme-ui";

import { TicketItem } from "~/types";

import { Button } from "../button/button";

type SelectedProduct = {
  id: string;
  variation?: string;
};

export const ProductSelectedVariationsList: React.SFC<{
  product: TicketItem;
  selectedProducts: {
    [id: string]: SelectedProduct[];
  };
  removeProduct: (id: string, variation: string) => void;
}> = ({ product, selectedProducts, removeProduct }) => {
  const productsToShow = Object.values(selectedProducts).filter(
    (p) => p.length > 0 && p[0].variation,
  );

  return (
    <React.Fragment>
      {productsToShow.map((selectedProduct) => {
        const groups = selectedProduct.reduce<{
          [variation: string]: SelectedProduct[];
        }>((current, product: SelectedProduct) => {
          const variation = product.variation!;

          if (!current[variation]) {
            current[variation] = [];
          }

          current[variation].push(product);
          return current;
        }, {});

        return Object.values(groups).map((group) => {
          const firstProduct = group[0];

          // we only want to show variation for this specific product
          if (firstProduct.id !== product.id) {
            return null;
          }

          return (
            <Grid
              sx={{ gridTemplateColumns: "1fr 50px", my: 3 }}
              key={`${firstProduct.id}${firstProduct.variation}`}
            >
              <Flex sx={{ display: "flex", alignItems: "center" }}>
                <Box>
                  <strong>{group.length}x</strong> {product.name}{" "}
                  <strong>
                    (
                    {
                      product.variations?.find(
                        (variation) => variation.id === firstProduct.variation,
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
        });
      })}
    </React.Fragment>
  );
};
