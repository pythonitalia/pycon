/** @jsx jsx */
import {
  Box,
  Button,
  Flex,
  Grid,
  Input,
  Select,
  Text,
} from "@theme-ui/components";
import React, { useEffect, useState } from "react";
import { useFormState } from "react-use-form-state";
import { jsx } from "theme-ui";

import { InputWrapper } from "../input-wrapper";

type Ticket = {
  name: string;
  id: string;
  defaultPrice: string;
  description?: string | null;
  variations?: { id: string; value: string; defaultPrice: string }[];
};

type Props = {
  tickets: Ticket[];
  onTicketsUpdate: (values: { [key: string]: number }) => void;
};

const ProductRow: React.SFC<{ ticket: Ticket }> = ({ ticket }) => {
  const hasVariation = ticket.variations && ticket.variations.length > 0;

  const [selected, setSelected] = useState<string[]>([]);
  const [currentVariation, setCurrentVariation] = useState("");

  const variationsById = hasVariation
    ? Object.fromEntries(
        ticket.variations!.map(variation => [variation.id, variation.value]),
      )
    : {};

  const addVariation = () =>
    currentVariation && setSelected(selected.concat([currentVariation]));
  const removeVariation = (index: number) =>
    setSelected(selected.filter((_, i) => i !== index));

  console.log(selected);

  return (
    <InputWrapper label={ticket.name}>
      <Grid
        sx={{
          gridTemplateColumns: "1fr 200px",
        }}
      >
        <Box sx={{ pl: 3 }}>
          <Text>
            Price:{" "}
            <Text as="span" sx={{ fontWeight: "bold" }}>
              {ticket.defaultPrice} EUR
            </Text>
          </Text>

          <Text>{ticket.description}</Text>
        </Box>

        <Flex
          sx={{ alignItems: "flex-start", justifyContent: "flex-end", pr: 3 }}
        >
          {hasVariation && (
            <Select
              sx={{ mr: 3, width: 100 }}
              onChange={(event: React.ChangeEvent<HTMLSelectElement>) =>
                setCurrentVariation(event.target.value)
              }
            >
              <option disabled={true} selected={!currentVariation}>
                select an option
              </option>
              {ticket.variations!.map(variation => (
                <option
                  key={variation.id}
                  value={variation.id}
                  selected={currentVariation === variation.id}
                >
                  {variation.value}
                </option>
              ))}
            </Select>
          )}

          {!hasVariation && (
            <Input defaultValue={0} min={0} sx={{ width: 50 }} />
          )}
          {hasVariation && <Button onClick={addVariation}>Add one</Button>}
        </Flex>
      </Grid>

      <Box sx={{ px: 3 }}>
        {hasVariation &&
          selected.map((variantId, index) => (
            <Grid sx={{ gridTemplateColumns: "1fr 140px", mt: 3 }} key={index}>
              <Box>
                {ticket.name} <strong>({variationsById[variantId]})</strong>
              </Box>
              <Button variant="small" onClick={() => removeVariation(index)}>
                Remove
              </Button>
            </Grid>
          ))}
      </Box>
    </InputWrapper>
  );
};

export const TicketsForm: React.SFC<Props> = ({ tickets, onTicketsUpdate }) => {
  // eslint-disable-next-line @typescript-eslint/tslint/config
  const [formState, { number }] = useFormState(
    Object.fromEntries(tickets.map(ticket => [ticket.id, 0])),
    {
      withIds: true,
    },
  );

  useEffect(() => onTicketsUpdate(formState.values), [formState.values]);

  return (
    <React.Fragment>
      {tickets.map(ticket => (
        <Box key={ticket.id}>
          <ProductRow ticket={ticket} />
        </Box>
      ))}
    </React.Fragment>
  );
};
