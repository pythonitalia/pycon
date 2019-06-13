import * as React from 'react';
import { useEffect, useState, useRef, useCallback, useMemo } from 'react';
import { RouteComponentProps } from '@reach/router';
import { Mutation, Query, MutationFn } from 'react-apollo';

import TICKETS from './get-tickets.graphql';
import BuyTicket from './buy-tickets.graphql';

import {
  BuyTicketWithStripe,
  buyTicketWithStripeVariables,
} from './Types/BuyTicketWithStripe';
import { Tickets, Tickets_conference_ticketFares } from './Types/Tickets';

import * as styles from './style.css';

// dummy example of the stripe integration
// don't do this at home?

type CartItem = {
  id: string;
  name: string;
  price: number;
  quantity: number;
};

type Cart = {
  [key: string]: CartItem;
};

const useStripe = (): any => {
  const stripe = window.Stripe('pk_test_1Tti9s1UY4Ot4NJXxWc6kdYg');
  return useMemo(() => stripe, []);
};

export const Payments = (props: RouteComponentProps) => {
  const [cart, setCart] = useState<Cart>({});
  const addCartItem = useCallback(
    (
      e: React.MouseEvent<HTMLElement>,
      ticket: Tickets_conference_ticketFares,
    ) => {
      setCart({
        ...cart,
        [ticket.code]: {
          id: ticket.id,
          name: ticket.name,
          price: ticket.price,
          quantity: (cart[ticket.code] ? cart[ticket.code].quantity : 0) + 1,
        },
      });
    },
    [cart],
  );
  const reduceCartQuantity = useCallback(
    (e: React.MouseEvent<HTMLElement>, code: string) => {
      setCart({
        ...cart,
        [code]: {
          ...cart[code],
          quantity: (cart[code] ? cart[code].quantity : 0) - 1,
        },
      });
    },
    [cart],
  );

  console.log('cart:', cart);
  return (
    <div className={styles.container}>
      <Listing addCartItem={addCartItem} className={styles.listing} />
      <Sidebar reduceCartQuantity={reduceCartQuantity} cart={cart} />
    </div>
  );
};

type SidebarProps = {
  className?: string;
  cart: Cart;
  reduceCartQuantity: (e: React.MouseEvent<HTMLElement>, code: string) => void;
};

const Sidebar = (props: SidebarProps) => {
  const { cart, reduceCartQuantity } = props;
  const total = calculateTotal(cart);

  return (
    <div className={styles.sidebar}>
      <Cart reduceCartQuantity={reduceCartQuantity} cart={cart} />

      <h2 className={styles.totalToPay}>
        Total to pay
        <span>{total}€</span>
      </h2>

      <h2>Pay using Stripe</h2>
      <Checkout cart={props.cart} />
    </div>
  );
};

type CheckoutProps = {
  cart: Cart;
};

const Checkout = (props: CheckoutProps) => {
  const stripe = useStripe();
  const elements = stripe.elements();
  const cardElement = elements.create('card', {
    iconStyle: 'solid',
    style: {
      base: {
        iconColor: '#c4f0ff',
        color: '#fff',
        fontWeight: 500,
        fontSize: '16px',
        fontSmoothing: 'antialiased',
        ':-webkit-autofill': {
          color: '#fff',
        },
        '::placeholder': {
          color: '#fff',
        },
      },
    },
  });
  const cardContainer = useRef(null);

  useEffect(() => {
    if (!cardContainer || !cardContainer.current) {
      return;
    }

    cardElement.mount(cardContainer.current);
  }, [Math.random()]);

  const { cart } = props;

  return (
    <div>
      <Mutation<BuyTicketWithStripe, buyTicketWithStripeVariables>
        mutation={BuyTicket}
      >
        {(buyTicketWithStripe, { data }) => {
          console.log('buyTicketWithStripe', buyTicketWithStripe, data);
          return (
            <React.Fragment>
              <div ref={cardContainer} />
              <StripeCheckout
                cardElement={cardElement}
                stripe={stripe}
                data={data}
                cart={cart}
                buyTicketWithStripe={buyTicketWithStripe}
              />
              <p>
                <br />
                Default US card:
                <br />
                4242424242424242
                <br />
                <br />
                3D Secure auth required:
                <br />
                4000000000003063
              </p>
            </React.Fragment>
          );
        }}
      </Mutation>
    </div>
  );
};

type StripeCheckoutProps = {
  cart: Cart;
  buyTicketWithStripe: MutationFn<
    BuyTicketWithStripe,
    buyTicketWithStripeVariables
  >;
  data: BuyTicketWithStripe;
  stripe: any;
  cardElement: any;
};

const StripeCheckout = (props: StripeCheckoutProps) => {
  const { cart, buyTicketWithStripe, data, stripe, cardElement } = props;

  useEffect(() => {
    console.log('data', data);

    if (!data) {
      return;
    }

    if (data.buyTicketWithStripe.__typename !== 'StripeClientSecret') {
      return;
    }

    const clientSecret = data.buyTicketWithStripe.clientSecret;

    const runPayment = async () => {
      const { paymentIntent, error } = await stripe.handleCardPayment(
        clientSecret,
        cardElement,
        {
          payment_method_data: {
            billing_details: {},
          },
        },
      );

      console.log('paymentIntent:', paymentIntent)
      console.log('error:', error)
    };

    runPayment();
  }, [data]);

  return (
    <button
      onClick={async e => {
        buyTicketWithStripe({
          variables: {
            input: {
              items: Object.keys(cart).map(code => ({
                id: cart[code].id,
                quantity: cart[code].quantity,
              })),
              conference: 'pypizza19',
            },
          },
        });
      }}
    >
      Checkout
    </button>
  );
};

function calculateTotal(cart: Cart) {
  return Object.keys(cart).reduce(
    (p, c) => p + cart[c].price * cart[c].quantity,
    0,
  );
}

type CardProps = {
  cart: Cart;
  reduceCartQuantity: (e: React.MouseEvent<HTMLElement>, code: string) => void;
};

const Cart = (props: CardProps) => {
  const { cart, reduceCartQuantity } = props;
  return (
    <div>
      <h2>Your cart</h2>

      <ul className={styles.cartItems}>
        {Object.keys(cart)
          .filter(code => cart[code].quantity > 0)
          .map(code => (
            <li key={code} className={styles.cartItem}>
              <span className={styles.cartItemName}>{cart[code].name}</span>
              <span className={styles.cartItemPrice}>{cart[code].price}€</span>
              <span className={styles.amount}>x{cart[code].quantity}</span>
              <span
                onClick={e => reduceCartQuantity(e, code)}
                className={styles.remove}
              >
                −
              </span>
            </li>
          ))}
      </ul>
    </div>
  );
};

type ListingProps = {
  className: string;
  addCartItem?: (
    e: React.MouseEvent<HTMLElement>,
    ticket: Tickets_conference_ticketFares,
  ) => void;
};

const Listing = (props: ListingProps) => {
  return (
    <div className={props.className}>
      <Query<Tickets> query={TICKETS}>
        {({ loading, error, data }) => {
          if (loading) {
            return <p>loading</p>;
          }

          console.log('data', data.conference.ticketFares);
          return (
            <TicketsListing
              addCartItem={props.addCartItem}
              tickets={data.conference.ticketFares}
            />
          );
        }}
      </Query>
    </div>
  );
};

type TicketsListingProps = {
  tickets: Tickets_conference_ticketFares[];
  addCartItem?: (
    e: React.MouseEvent<HTMLElement>,
    ticket: Tickets_conference_ticketFares,
  ) => void;
};

type TicketGroups = {
  [key: string]: Tickets_conference_ticketFares[];
};

type Mapper = {
  [key: string]: string;
};

const TicketsListing = (props: TicketsListingProps) => {
  const ticketsGroup = createTicketsGroup(props.tickets);

  // Object.entries does not exists on typescript now, we've to update the configuration but..
  // it's not worth lol
  return (
    <ul className={styles.ticketsListing}>
      {Object.keys(ticketsGroup).map(title => {
        const tickets = ticketsGroup[title];
        return (
          <li key={title} className={styles.ticketGroup}>
            <h2>{title}</h2>
            <div className={styles.groupTickets}>
              {tickets.map(ticket => (
                <TicketCard
                  key={ticket.code}
                  onClick={props.addCartItem}
                  ticket={ticket}
                />
              ))}
            </div>
          </li>
        );
      })}
    </ul>
  );
};

const createTicketsGroup = (
  tickets: Tickets_conference_ticketFares[],
): TicketGroups => {
  const groups: TicketGroups = {
    'Early Bird': [],
    Regular: [],
    Late: [],
    Socials: [],
  };
  const mapper: Mapper = {
    ebr: 'Early Bird',
    ebs: 'Early Bird',
    ebe: 'Early Bird',
    pybeer: 'Socials',
    pydinner: 'Socials',
  };

  tickets.forEach(ticket => {
    groups[mapper[ticket.code]].push(ticket);
  });

  return groups;
};

type TicketCardProps = {
  ticket: Tickets_conference_ticketFares;
  onClick?: (
    e: React.MouseEvent<HTMLElement>,
    ticket: Tickets_conference_ticketFares,
  ) => void;
};

const TicketCard = (props: TicketCardProps) => {
  const { ticket, onClick } = props;
  return (
    <div onClick={e => onClick(e, ticket)} className={styles.ticketCard}>
      <h3 className={styles.name}>{ticket.name}</h3>
      <p className={styles.description}>{ticket.description}</p>
      <span className={styles.price}>{ticket.price}€</span>
    </div>
  );
};
