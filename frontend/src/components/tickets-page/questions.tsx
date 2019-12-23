/** @jsx jsx */
import { Box, Button, Heading, Input, Select } from "@theme-ui/components";
import React from "react";
import { jsx } from "theme-ui";

import { InputWrapper } from "../input-wrapper";
import { Ticket } from "../tickets-form/types";
import { SelectedProducts } from "./types";

type Props = {
  path: string;
  tickets: Ticket[];
  selectedProducts: SelectedProducts;
  onNextStep: () => void;
};

export const QuestionsSection: React.SFC<Props> = ({
  tickets,
  selectedProducts,
  onNextStep,
}) => {
  const productsById = Object.fromEntries(
    tickets.map(product => [product.id, product]),
  );

  return (
    <React.Fragment>
      <Heading sx={{ mb: 3 }}>Order questions</Heading>

      {Object.entries(selectedProducts)
        .filter(([_, product]) => product.quantity > 0)
        .map(([id, selectedProduct]) => (
          <Box key={id}>
            {new Array(selectedProduct.quantity).fill(null).map((_, index) => {
              const product = productsById[selectedProduct.id];

              if (product.questions.length === 0) {
                return null;
              }

              return (
                <Box key={`${id}${index}`}>
                  <Heading sx={{ fontSize: 2, mb: 2 }}>
                    {index + 1}. {product.name}
                  </Heading>

                  {product.questions.map(question => (
                    <Box key={question.id}>
                      <InputWrapper label={question.name}>
                        {question.options.length === 0 ? (
                          <Input />
                        ) : (
                          <Select>
                            {question.options.map(option => (
                              <option key={option.id} value={option.id}>
                                {option.name}
                              </option>
                            ))}
                          </Select>
                        )}
                      </InputWrapper>
                    </Box>
                  ))}
                </Box>
              );
            })}
          </Box>
        ))}

      <Button onClick={onNextStep}>Next step</Button>
    </React.Fragment>
  );
};
