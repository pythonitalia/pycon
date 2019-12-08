/** @jsx jsx */
import { Box, Grid, Input, Text } from "@theme-ui/components";
import React, { useEffect } from "react";
import { useFormState } from "react-use-form-state";
import { jsx } from "theme-ui";

import { InputWrapper } from "../input-wrapper";

type Ticket = {
  name: string;
  id: string;
  defaultPrice: string;
  description?: string | null;
};

type Props = {
  tickets: Ticket[];
  onTicketsUpdate: (values: { [key: string]: number }) => void;
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
          <InputWrapper label={ticket.name}>
            <Grid
              sx={{
                gridTemplateColumns: "1fr 100px",
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

              <Input {...number(ticket.id)} defaultValue={0} min={0} />
            </Grid>
          </InputWrapper>
        </Box>
      ))}
    </React.Fragment>
  );
};
