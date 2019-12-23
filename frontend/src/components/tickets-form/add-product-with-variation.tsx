/** @jsx jsx */
import { Button, Flex, Select } from "@theme-ui/components";
import React, { useState } from "react";
import { jsx } from "theme-ui";

import { Ticket } from "./types";

export const AddProductWithVariation: React.SFC<{
  ticket: Ticket;
  addVariation: (variationId: string) => void;
}> = ({ ticket, addVariation }) => {
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
        <option disabled={true} selected={!currentVariation}>
          Select...
        </option>
        {ticket.variations!.map(variation => (
          <option key={variation.id} value={variation.id}>
            {variation.value}
          </option>
        ))}
      </Select>

      <Button
        onClick={() => addVariation(currentVariation)}
        variant="plus"
        sx={{ ml: 3 }}
      >
        +
      </Button>
    </Flex>
  );
};
