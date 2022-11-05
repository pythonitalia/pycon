/** @jsxRuntime classic */

/** @jsx jsx */
import React, { useState } from "react";
import { FormattedMessage } from "react-intl";
import { Flex, jsx, Select } from "theme-ui";

import { TicketItem } from "~/types";

import { Button } from "../button/button";

export const AddProductWithVariation = ({
  ticket,
  addVariation,
}: {
  ticket: TicketItem;
  addVariation: (variationId: string) => void;
}) => {
  const [currentVariation, setCurrentVariation] = useState("");

  return (
    <Flex sx={{ justifyContent: ["", "space-between"] }}>
      <Select
        value={currentVariation}
        sx={{ width: 120, height: 50 }}
        onChange={(event: React.ChangeEvent<HTMLSelectElement>) =>
          setCurrentVariation(event.target.value)
        }
      >
        <FormattedMessage id="order.selectSize">
          {(text) => (
            <option disabled={true} value="">
              {text}
            </option>
          )}
        </FormattedMessage>
        {ticket.variations!.map((variation) => (
          <option key={variation.id} value={variation.id}>
            {variation.value}
          </option>
        ))}
      </Select>

      <Button
        onClick={() => {
          if (currentVariation === "") {
            return;
          }

          addVariation(currentVariation);
        }}
        variant="plus"
        sx={{ ml: 3 }}
      >
        +
      </Button>
    </Flex>
  );
};
