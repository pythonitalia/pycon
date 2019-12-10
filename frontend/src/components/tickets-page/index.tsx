/** @jsx jsx */
import { useMutation, useQuery } from "@apollo/react-hooks";
import { Box, Button, Heading, Text } from "@theme-ui/components";
import React, { useCallback, useContext, useEffect, useState } from "react";
import { FormattedMessage } from "react-intl";
import { jsx } from "theme-ui";

import { ConferenceContext } from "../../context/conference";
import { useCurrentLanguage } from "../../context/language";
import {
  CreateOrderMutation,
  CreateOrderMutationVariables,
  TicketsQuery,
  TicketsQueryVariables,
} from "../../generated/graphql-backend";
import { MetaTags } from "../meta-tags";
import CREATE_ORDER_MUTATION from "./create-order.graphql";
import { HotelForm } from "./hotel-form";
import { TicketsForm } from "./tickets-form";
import TICKETS_QUERY from "./tickets.graphql";

export const TicketsPage: React.SFC = () => {
  const conferenceCode = useContext(ConferenceContext);
  const language = useCurrentLanguage();

  const [createOrder, { data: orderData }] = useMutation<
    CreateOrderMutation,
    CreateOrderMutationVariables
  >(CREATE_ORDER_MUTATION, {
    onCompleted(result) {
      if (result.createOrder.__typename !== "CreateOrderResult") {
        return;
      }

      window.location.href = `${
        result.createOrder.paymentUrl
      }?return_url=${encodeURIComponent(
        window.location.origin,
      )}/${language}/profile`;
    },
  });

  const { loading, error, data } = useQuery<
    TicketsQuery,
    TicketsQueryVariables
  >(TICKETS_QUERY, {
    variables: {
      conference: conferenceCode,
      language,
    },
  });

  const [selectedTickets, setSelectedTickets] = useState({});

  const createOrderCallback = useCallback(
    paymentProvider => {
      const orderTickets = Object.entries(selectedTickets).map(
        ([id, total]) => ({
          ticketId: id,
          total: Number(total),
        }),
      );

      createOrder({
        variables: {
          input: {
            paymentProvider,
            tickets: orderTickets,
            email: "patrick.arminio@gmail.com",
            locale: language,
          },
        },
      });
    },
    [selectedTickets],
  );

  if (error) {
    throw new Error(error.message);
  }

  const tickets = data?.conference.tickets;

  return (
    <Box>
      <FormattedMessage id="tickets.pageTitle">
        {text => <MetaTags title={text} />}
      </FormattedMessage>

      <Box
        sx={{
          maxWidth: "container",
          mx: "auto",
          px: 3,
        }}
      >
        {loading && (
          <Text>
            <FormattedMessage id="tickets.loading" />
          </Text>
        )}

        {!loading && (
          <React.Fragment>
            <Heading sx={{ mb: 3 }}>Get some tickets</Heading>
            {tickets && (
              <TicketsForm
                tickets={tickets}
                onTicketsUpdate={setSelectedTickets}
              />
            )}

            <Button onClick={() => createOrderCallback("stripe")}>
              Pay with stripe
            </Button>
          </React.Fragment>
        )}
      </Box>
    </Box>
  );
};

// <Heading sx={{ mb: 3 }}>Book your hotel room!</Heading>
// <HotelForm />
