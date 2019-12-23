/** @jsx jsx */
import { useMutation } from "@apollo/react-hooks";
import { Box, Button, Flex, Heading, Text } from "@theme-ui/components";
import React, { Fragment, useCallback, useContext } from "react";
import { FormattedMessage } from "react-intl";
import { jsx } from "theme-ui";

import { ConferenceContext } from "../../context/conference";
import { useCurrentLanguage } from "../../context/language";
import {
  CreateOrderMutation,
  CreateOrderMutationVariables,
} from "../../generated/graphql-backend";
import { Alert } from "../alert";
import CREATE_ORDER_MUTATION from "./create-order.graphql";
import { OrderState, SelectedProducts } from "./types";

type Props = {
  state: OrderState;
  email: string;
};

export const CreateOrderButtons: React.SFC<Props> = ({ state, email }) => {
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

  const createOrderCallback = useCallback(
    paymentProvider => {
      const orderTickets = Object.values(
        state.selectedProducts as SelectedProducts,
      )
        .flat()
        .map(product => ({
          ticketId: product.id,
          variation: product.variation,
          attendeeName: product.attendeeName,
          attendeeEmail: product.attendeeEmail,
          answers: Object.entries(product.answers).map(([key, value]) => ({
            questionId: key,
            value,
          })),
        }));

      createOrder({
        variables: {
          conference: conferenceCode,

          input: {
            paymentProvider,
            tickets: orderTickets,
            email,
            locale: language,
            invoiceInformation: {
              isBusiness: state.invoiceInformation.isBusiness === "true",
              company: state.invoiceInformation.companyName,
              name: state.invoiceInformation.name,
              street: state.invoiceInformation.address,
              zipcode: state.invoiceInformation.zipCode,
              city: state.invoiceInformation.city,
              country: state.invoiceInformation.country,
              vatId: state.invoiceInformation.vatId,
              fiscalCode: state.invoiceInformation.fiscalCode,
            },
          },
        },
      });
    },
    [state],
  );

  const hasOrder = orderData?.createOrder.__typename === "CreateOrderResult";
  const orderErrorMessage =
    orderData?.createOrder.__typename === "Error" &&
    orderData.createOrder.message;

  return (
    <Fragment>
      {orderErrorMessage && <Alert variant="alert">{orderErrorMessage}</Alert>}

      {(creatingOrder || hasOrder) && (
        <Alert variant="info">
          <FormattedMessage id="order.creatingOrder" />
        </Alert>
      )}

      {!creatingOrder && !hasOrder && (
        <Fragment>
          <Button sx={{ mr: 2 }} onClick={() => createOrderCallback("stripe")}>
            <FormattedMessage id="order.payWithCard" />
          </Button>

          <Button onClick={() => createOrderCallback("banktransfer")}>
            <FormattedMessage id="order.payWithBankTransfer" />
          </Button>
        </Fragment>
      )}
    </Fragment>
  );
};
