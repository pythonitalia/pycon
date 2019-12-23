/** @jsx jsx */
import { Box, Button, Heading, Text, Flex } from "@theme-ui/components";
import React, { Fragment, useCallback, useContext } from "react";
import { jsx } from "theme-ui";
import { OrderState, SelectedProducts } from "./types";
import { useMutation } from "@apollo/react-hooks";
import CREATE_ORDER_MUTATION from "./create-order.graphql";
import {
  CreateOrderMutation,
  CreateOrderMutationVariables,
} from "../../generated/graphql-backend";
import { ConferenceContext } from "../../context/conference";
import { useCurrentLanguage } from "../../context/language";

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

      console.log("email:", email, "fdffd", {
        paymentProvider,
        tickets: orderTickets,
        email: email,
        locale: language,
      });

      createOrder({
        variables: {
          conference: conferenceCode,

          input: {
            paymentProvider,
            tickets: orderTickets,
            email: email,
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
      <Button sx={{ mr: 2 }} onClick={() => createOrderCallback("stripe")}>
        Pay with stripe
      </Button>

      <Button onClick={() => createOrderCallback("banktransfer")}>
        Pay with bank transfer
      </Button>
    </Fragment>
  );
};
