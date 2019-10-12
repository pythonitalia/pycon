import { useQuery } from "@apollo/react-hooks";
import { RouteComponentProps } from "@reach/router";
import React, { useState } from "react";

import {
  ConferenceTicketsQuery,
  ConferenceTicketsQueryVariables,
} from "../../generated/graphql-backend";
import { StripeCheckout } from "../stripe-checkout";
import { Tickets } from "./tickets";
import CONFERENCE_TICKETS_QUERY from "./ticketsList.graphql";

export type Cart = {
  [key: string]: number;
};

export const BuyTickets: React.SFC<RouteComponentProps<{}>> = ({}) => {
  const [cart, setCart] = useState<Cart>({});
  const { loading, error, data: ticketsData } = useQuery<
    ConferenceTicketsQuery,
    ConferenceTicketsQueryVariables
  >(CONFERENCE_TICKETS_QUERY, { variables: { code: "pycon-demo" } });

  return (
    <div>
      {loading && (
        <p>Please wait while we fetch the list of tickets available 👀</p>
      )}
      {!loading && error && <p>Oppsie cannot get the tickets</p>}
      {!loading && ticketsData && (
        <>
          <h2>Tickets</h2>
          <Tickets
            cart={cart}
            updateCart={setCart}
            tickets={ticketsData.conference.ticketFares}
          />
          <h2>Checkout</h2>
          <StripeCheckout cart={cart} />
        </>
      )}
    </div>
  );
};
