import * as React from 'react';
import { useEffect, useState, useRef, useCallback } from 'react';
import { RouteComponentProps } from '@reach/router';
import { Mutation } from "react-apollo";

import BuyTicketWithStripe from './query.graphql'

import * as styles from './style.css';

// dummy example of the stripe integration

/* Publishable key */

// const useStripeToken = () => {
//   const [token, setToken] = useState(null);

//   useEffect(() => {
//   }, []);
// }
const useStripe = container => {
  const [stripe, setStripe] = useState(null);
  const [cardElement, setCardElement] = useState(null);
  const onStripeReadyHandler = useCallback(() => {
    const obj = window.Stripe('pk_test_1Tti9s1UY4Ot4NJXxWc6kdYg');
    setStripe(obj);
  }, []);

  useEffect(() => {
    if (!container || !container.current) {
      return;
    }

    if (!stripe) {
      return;
    }

    console.log('container:', container)

    const elements = stripe.elements();
    const cElement = elements.create('card');
    cElement.mount(container.current);
    setCardElement(cElement);
  }, [container, stripe]);

  useEffect(() => {
    const exists = document.querySelector('script[src="https://js.stripe.com/v3/"]');

    if (exists) {
      // call onStripeReadyHandler maybe
      return;
    }

    const js = document.createElement('script');
    js.src = 'https://js.stripe.com/v3/';
    js.onload = onStripeReadyHandler;
    document.head.appendChild(js);
  }, []);

  return [stripe, cardElement];
};

export const Payments = (props: RouteComponentProps) => {
  const paymentDataContainerRef = useRef(null);
  const [ stripe, cardElement ] = useStripe(paymentDataContainerRef);

  return <div className={styles.Container}>
    <p>Hello! Payment test screen! 💰</p>

    <p>success card:</p>
    <p>4242424242424242 Visa</p>

    <p>3d card</p>
    <p>4000000000003220</p>

    <div ref={paymentDataContainerRef}></div>
    <Mutation mutation={BuyTicketWithStripe}>
      {(buyTicketWithStripe, { data, loading, error }) => {
        if (loading) {
          return <p>Loading!</p>;
        }

        if (error) {
          return <p>Something went wrong :(</p>
        }

        console.log('data', data)

        // refactor
        if (data && data.buyTicketWithStripe && data.buyTicketWithStripe.__typename === 'Stripe3DValidationRequired') {
          stripe.handleCardAction(data.buyTicketWithStripe.clientSecret).then(result => {
            if (result.error) {
              console.log('error', result.error)
              return;
            }

            buyTicketWithStripe({
              variables: {
                input: {
                  conference: "pypizza19",
                  items: [{ quantity: 2, id: 1 }],
                  paymentIntentId: result.paymentIntent.id,
                },
              },
            });
          });
        }

        return <div>
          <button onClick={async e => {
            e.preventDefault();

            const { paymentMethod } = await stripe.createPaymentMethod('card', cardElement, {})

            console.log('buyTicketWithStripe', buyTicketWithStripe, paymentMethod)

            buyTicketWithStripe({
              variables: {
                input: {
                  conference: "pypizza19",
                  items: [{ quantity: 2, id: 1 }],
                  paymentMethodId: paymentMethod.id,
                },
              },
            });
          }}>
            Pay
          </button>
        </div>;
      }}
    </Mutation>
  </div>;
};
