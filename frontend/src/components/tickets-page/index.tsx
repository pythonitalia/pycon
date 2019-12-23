/** @jsx jsx */
import { useMutation, useQuery } from "@apollo/react-hooks";
import { RouteComponentProps, Router } from "@reach/router";
import { Box, Text } from "@theme-ui/components";
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
import CREATE_ORDER_MUTATION from "./create-order.graphql";
import { InformationSection } from "./information";
import { QuestionsSection } from "./questions";
import { reducer } from "./reducer";
import { TicketsSection } from "./tickets";
import TICKETS_QUERY from "./tickets.graphql";
import { SelectedProducts } from "./types";

export const TicketsPage: React.SFC<RouteComponentProps> = props => {
  const conferenceCode = useContext(ConferenceContext);
  const language = useCurrentLanguage();

  const [
    createOrder,
    { data: orderData, loading: creatingOrder },
  ] = useMutation<CreateOrderMutation, CreateOrderMutationVariables>(
    CREATE_ORDER_MUTATION,
    {
      onCompleted(result) {
        if (result.createOrder.__typename !== "CreateOrderResult") {
          return;
        }

        window.location.href = result.createOrder.paymentUrl;
      },
    },
  );

  const hasOrder = orderData?.createOrder.__typename === "CreateOrderResult";
  const orderErrorMessage =
    orderData?.createOrder.__typename === "Error" &&
    orderData.createOrder.message;

  const { loading, error, data } = useQuery<
    TicketsQuery,
    TicketsQueryVariables
  >(TICKETS_QUERY, {
    variables: {
      conference: conferenceCode,
      language,
    },
  });

  const [state, dispatcher] = useReducer(reducer, {
    selectedProducts: {},
    invoiceInformation: null,
  });

  const createOrderCallback = useCallback(
    paymentProvider => {
      const orderTickets = Object.values(
        state.selectedProducts as SelectedProducts,
      )
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

  const tickets = data?.conference.tickets || [];

  const addProduct = (id: string, variation?: string) =>
    dispatcher({
      type: "incrementProduct",
      id,
      variation,
    });

  const removeProduct = (id: string, variation?: string) =>
    dispatcher({
      type: "decrementProduct",
      id,
      variation,
    });

  console.log(state);

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
          <Router>
            <TicketsSection
              default={true}
              tickets={tickets}
              selectedProducts={state.selectedProducts}
              addProduct={addProduct}
              removeProduct={removeProduct}
              onNextStep={() => props.navigate!("information")}
            />
            <InformationSection
              path="information"
              onUpdateInformation={invoiceData =>
                dispatcher({
                  type: "updateInvoiceInformation",
                  data: invoiceData,
                })
              }
              onNextStep={() => props.navigate!("questions")}
            />
            <QuestionsSection
              path="questions"
              tickets={tickets}
              selectedProducts={state.selectedProducts}
              onNextStep={() => props.navigate!("questions")}
            />
          </Router>
        )}
      </Box>
    </Box>
  );
};

// {orderErrorMessage && (
//   <Alert variant="alert">{orderErrorMessage}</Alert>
// )}

// {creatingOrder || hasOrder ? (
//   <Box>Creating order...</Box>
// ) : (
//   <React.Fragment>
//     <Button
//       sx={{ mr: 2 }}
//       onClick={() => createOrderCallback("stripe")}
//     >
//       Pay with stripe
//     </Button>

//     <Button onClick={() => createOrderCallback("banktransfer")}>
//       Pay with bank transfer
//     </Button>
//   </React.Fragment>
// )}
