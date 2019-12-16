/** @jsx jsx */
import { useMutation, useQuery } from "@apollo/react-hooks";
import { RouteComponentProps } from "@reach/router";
import { Box, Button, Heading, Text } from "@theme-ui/components";
import React, { useCallback, useContext, useReducer } from "react";
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
import { TicketsForm } from "../tickets-form";
import CREATE_ORDER_MUTATION from "./create-order.graphql";
import { reducer } from "./reducer";
import TICKETS_QUERY from "./tickets.graphql";

export const TicketsPage: React.SFC<RouteComponentProps> = () => {
  const conferenceCode = useContext(ConferenceContext);
  const language = useCurrentLanguage();

  // TODO: error handling
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

  const [state, dispatcher] = useReducer(reducer, {});

  const createOrderCallback = useCallback(
    paymentProvider => {
      const orderTickets = Object.values(state)
        .filter(product => product.quantity > 0)
        .map(product => ({
          ticketId: product.id,
          quantity: product.quantity,
          variation: product.variation,
        }));

      createOrder({
        variables: {
          conference: conferenceCode,

          input: {
            paymentProvider,
            tickets: orderTickets,
            email: data?.me.email!,
            locale: language,
          },
        },
      });
    },
    [state],
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
                selectedProducts={state}
                addProduct={(id: string, variation?: string) =>
                  dispatcher({
                    type: "increment",
                    id,
                    variation,
                  })
                }
                removeProduct={(id: string, variation?: string) =>
                  dispatcher({
                    type: "decrement",
                    id,
                    variation,
                  })
                }
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
