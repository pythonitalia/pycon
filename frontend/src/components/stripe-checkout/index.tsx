import React, { useCallback, useContext, useRef, useState } from "react";
import { Button } from "../button";
import styled from "styled-components";
import { useMutation } from "@apollo/react-hooks";
import { Helmet } from "react-helmet";

import {
  BuyTicketsMutation,
  BuyTicketsMutationVariables,
} from "../../generated/graphql-backend";

import { EnvironmentContext } from "../../context/environment";

import BUY_TICKETS_MUTATION from "./buyTickets.graphql";

import { Cart } from "../buy-tickets";

type Props = {
  cart: Cart;
};

const stripeStyle = {
  base: {
    color: "#32325d",
    fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
    fontSmoothing: "antialiased",
    fontSize: "16px",
    "::placeholder": {
      color: "#aab7c4",
    },
  },
  invalid: {
    color: "#fa755a",
    iconColor: "#fa755a",
  },
};

const CardForm = styled.div<{ visible: boolean }>`
  opacity: ${props => (props.visible ? 1 : 0)};
  transition: opacity 150ms ease;

  .StripeElement {
    height: 40px;

    padding: 10px 12px;
    margin: 10px 0;

    border: 1px solid transparent;
    border-radius: 4px;
    background-color: white;

    box-shadow: 0 1px 3px 0 #e6ebf1;
    transition: box-shadow 150ms ease;
  }

  .StripeElement--focus {
    box-shadow: 0 1px 3px 0 #cfd7df;
  }

  .StripeElement--invalid {
    border-color: #fa755a;
  }

  .StripeElement--webkit-autofill {
    background-color: #fefde5 !important;
  }
`;

export const StripeCheckout: React.SFC<Props> = ({ cart }) => {
  const cardNumberRef = useRef(null);
  const cardElement = useRef(null);
  const environmentContext = useContext(EnvironmentContext);
  const stripe = useRef(null);
  const [visible, showUI] = useState(false);

  const onShowElements = useCallback(() => {
    stripe.current = new window.Stripe(environmentContext.stripePublishableKey);
    const elements = stripe.current.elements();

    cardElement.current = elements.create("card", { style: stripeStyle });
    cardElement.current.mount(cardNumberRef.current);

    showUI(true);
  }, []);

  const [
    buyTickets,
    {
      loading: buyTicketsLoading,
      error: buyTicketsError,
      data: buyTicketsData,
    },
  ] = useMutation<BuyTicketsMutation, BuyTicketsMutationVariables>(
    BUY_TICKETS_MUTATION,
  );

  const onPay = useCallback(async () => {
    console.log("stripe:", stripe.current);

    const response = await buyTickets({
      variables: {
        conference: "pycon-demo",
        cart: Object.entries(cart).reduce((p, [id, quantity]) => {
          p.push({ id, quantity });
          return p;
        }, []),
      },
    });

    const { data, errors } = response;

    if (data && data.buyTicketWithStripe.__typename === "StripeClientSecret") {
      const clientSecret = data.buyTicketWithStripe.clientSecret;
      const { paymentIntent, error } = await stripe.current.handleCardPayment(
        clientSecret,
        cardElement.current,
      );

      console.log("paymentIntent", paymentIntent);
      console.log("error:", error);
    }

    console.log("response:", response);
  }, [cart]);

  return (
    <div>
      <Helmet
        script={[
          {
            src: "https://js.stripe.com/v3/",
            type: "text/javascript",
          },
        ]}
      />

      <Button onClick={onShowElements}>Stripe Checkout</Button>
      <CardForm visible={visible}>
        <div ref={cardNumberRef}></div>
        <Button onClick={onPay}>Pay now</Button>
      </CardForm>
    </div>
  );
};
