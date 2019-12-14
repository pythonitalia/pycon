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

  const [quantity, setQuantity] = useState(0);

  console.log(selected);

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

        {hasVariation && (
          <Flex sx={{ justifyContent: ["", "space-between"] }}>
            <Select
              sx={{ width: 120, height: 50 }}
              onChange={(event: React.ChangeEvent<HTMLSelectElement>) =>
                setCurrentVariation(event.target.value)
              }
            >
              <option disabled={true} selected={!currentVariation}>
                Size
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

            <Button onClick={addVariation} variant="plus" sx={{ ml: 3 }}>
              +
            </Button>
          </Flex>
        )}

        {!hasVariation && (
          <Flex sx={{ justifyContent: "space-between" }}>
            <Button
              onClick={() => setQuantity(Math.max(0, quantity - 1))}
              variant="minus"
            >
              -
            </Button>
            <Input
              defaultValue={0}
              value={quantity}
              min={0}
              sx={{
                width: [100, 50],
                height: 50,
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
                textAlign: "center",
                p: 0,
              }}
            />
            <Button onClick={() => setQuantity(quantity + 1)} variant="plus">
              +
            </Button>
          </Flex>
        )}
      </Grid>

      {hasVariation &&
        selected.map((variantId, index) => (
          <Grid sx={{ gridTemplateColumns: "1fr 50px", mt: 3 }} key={index}>
            <Flex sx={{ display: "flex", alignItems: "center" }}>
              <Box>
                {ticket.name} <strong>({variationsById[variantId]})</strong>
              </Box>
            </Flex>
            <Button variant="minus" onClick={() => removeVariation(index)}>
              -
            </Button>
          </Grid>
        ))}
    </Box>
  );
};

export const TicketsForm: React.SFC<Props> = ({ tickets, onTicketsUpdate }) => {
  // eslint-disable-next-line @typescript-eslint/tslint/config
  const [formState] = useFormState(
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
