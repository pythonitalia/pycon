/** @jsx jsx */

import { Box, Button, Grid, Heading, Text } from "@theme-ui/components";
import { Fragment, useCallback, useState } from "react";
import { FormattedMessage } from "react-intl";
import { jsx, Styled } from "theme-ui";

const COLORS = ["violet", "keppel", "orange", "yellow"];

const TICKETS = [
  /* early */
  {
    name: "Student Early Bird",
    price: "50.00",
    from: "07/12/2019",
    until: "10/02/2020",
  },
  {
    name: "Personal Early Bird",
    price: "120.00",
    from: "07/12/2019",
    until: "10/02/2020",
  },
  {
    name: "Business Early Bird",
    price: "180.00",
    from: "07/12/2019",
    until: "10/02/2020",
  },
  /* regular */
  {
    name: "Student Regular",
    price: "80.00",
    from: "10/02/2020",
    until: "01/03/2020",
  },
  {
    name: "Personal Regular",
    price: "150.00",
    from: "10/02/2020",
    until: "01/03/2020",
  },
  {
    name: "Business Regular",
    price: "230.00",
    from: "10/02/2020",
    until: "01/03/2020",
  },
  /* late */
  {
    name: "Student Late",
    price: "100.00",
    from: "01/03/2020",
    until: "29/03/2020",
  },
  {
    name: "Personal Late",
    price: "190.00",
    from: "01/03/2020",
    until: "29/03/2020",
  },
  {
    name: "Business Late",
    price: "280.00",
    from: "01/03/2020",
    until: "29/03/2020",
  },
  /* on desk */
  {
    name: "Student On-Desk",
    price: "120.00",
    from: "29/03/2020",
    until: "05/04/2020",
  },
  {
    name: "Personal On-Desk",
    price: "220.00",
    from: "29/03/2020",
    until: "05/04/2020",
  },
  {
    name: "Business On-Desk",
    price: "320.00",
    from: "29/03/2020",
    until: "05/04/2020",
  },
];

type TableHeadProps = {
  position: number;
};

const TableHead: React.SFC<TableHeadProps> = ({ children, position }) => (
  <Text
    sx={{
      display: ["none", "block"],
      color: COLORS[position % COLORS.length],
      fontWeight: "bold",
      textAlign: [null, "center"],
      pb: 3,
      textTransform: "uppercase",
      borderBottom: "primary",
    }}
  >
    {children}
  </Text>
);

type TableRowProps = {
  className?: string;
};

const TableRow: React.SFC<TableRowProps> = ({ children, className }) => (
  <Text
    sx={{
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      textAlign: [null, "center"],
      p: 2,
      borderBottom: [null, "primary"],
    }}
    className={className}
  >
    {children}
  </Text>
);

export const Introduction = () => {
  const [ticketsTableOpen, setTicketsTableOpen] = useState(false);
  const toggleTicketsTable = useCallback(() => {
    setTicketsTableOpen(o => !o);
  }, []);

  return (
    <Grid
      sx={{
        gridTemplateColumns: [null, null, null, "0.6fr 1.4fr"],
        mb: 3,
      }}
    >
      <Box>
        <Heading sx={{ mb: 3 }}>
          <FormattedMessage id="tickets.heading" />
        </Heading>
        <Text>Buy your tickets here!</Text>

        <Button
          sx={{
            mt: 2,
            display: [null, "none"],
          }}
          onClick={toggleTicketsTable}
        >
          <FormattedMessage id="tickets.seeAllTickets" />
        </Button>
      </Box>
      <Grid
        sx={{
          gridTemplateColumns: ["1fr 1fr", "1fr 0.6fr 1fr 1fr"],
          gap: 0,
          borderBottom: ["primary", "none"],
          display: [ticketsTableOpen ? "" : "none", "grid"],
        }}
      >
        <TableHead position={0}>
          <FormattedMessage id="ticketsTable.name" />
        </TableHead>
        <TableHead position={1}>
          <FormattedMessage id="ticketsTable.price" />
        </TableHead>
        <TableHead position={2}>
          <FormattedMessage id="ticketsTable.from" />
        </TableHead>
        <TableHead position={3}>
          <FormattedMessage id="ticketsTable.until" />
        </TableHead>
        {TICKETS.map(ticket => (
          <Fragment key={ticket.name}>
            <TableRow
              key={ticket.name}
              sx={{
                borderRight: ["none", "primary"],
                borderLeft: ["primary", "none"],
                borderTop: ["primary", "none"],
                justifyContent: ["flex-start", "center"],
              }}
            >
              {ticket.name}
            </TableRow>
            <TableRow
              key={`${ticket.name}-${ticket.price}`}
              sx={{
                borderRight: ["primary", "none"],
                borderTop: ["primary", "none"],
                justifyContent: ["flex-end", "center"],
              }}
            >
              {ticket.price}€
            </TableRow>
            <TableRow
              key={`${ticket.from}-${ticket.name}`}
              sx={{
                borderLeft: ["primary", "null"],
                gridColumn: ["1 / 3", "auto"],
                borderRight: "primary",
                justifyContent: ["flex-start", "center"],
              }}
            >
              <Text
                sx={{
                  display: ["none", "block"],
                }}
              >
                {ticket.from}
              </Text>

              <Text
                sx={{
                  display: [null, "none"],
                }}
              >
                <FormattedMessage
                  id="ticketsTable.untilAndFromMobile"
                  values={{
                    from: <strong>{ticket.from}</strong>,
                    until: <strong>{ticket.until}</strong>,
                  }}
                />
              </Text>
            </TableRow>
            <TableRow
              key={`${ticket.name}-${ticket.until}`}
              sx={{
                display: ["none", "block"],
                borderRight: ["primary", "none"],
              }}
            >
              {ticket.until}
            </TableRow>
          </Fragment>
        ))}
      </Grid>
    </Grid>
  );
};
