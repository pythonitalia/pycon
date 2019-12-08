/** @jsx jsx */
import { Box, Grid, Input, Text } from "@theme-ui/components";
import React from "react";
import { jsx } from "theme-ui";

import { InputWrapper } from "../input-wrapper";

type Ticket = {
  name: string;
  id: string;
  defaultPrice: string;
  description: string | null;
};

type Props = {
  tickets: Ticket[];
};

export const TicketsForm: React.SFC<Props> = ({ tickets }) => {
  const x = 1;

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

              <Input type="number" defaultValue={0} min={0} />
            </Grid>
          </InputWrapper>
        </Box>
      ))}
    </React.Fragment>
  );
};
