import React from "react";

import { GetStaticProps } from "next";

import { addApolloState, getApolloClient } from "~/apollo/client";
import { CheckoutPageHandler } from "~/components/checkout-page-handler";
import { TicketsPageWrapper } from "~/components/tickets-page/wrapper";
import { prefetchSharedQueries } from "~/helpers/prefetch";
import { queryTickets } from "~/types";

export const TicketsCheckoutPage = () => {
  return (
    <TicketsPageWrapper>
      {({ tickets, hotelRooms, conference, me }) => (
        <CheckoutPageHandler
          me={me}
          conference={conference}
          products={tickets}
          hotelRooms={hotelRooms}
        />
      )}
    </TicketsPageWrapper>
  );
};

export const getStaticProps: GetStaticProps = async ({ locale }) => {
  const client = getApolloClient();

  await Promise.all([
    prefetchSharedQueries(client, locale),
    queryTickets(client, {
      conference: process.env.conferenceCode,
      language: "it",
    }),
    queryTickets(client, {
      conference: process.env.conferenceCode,
      language: "en",
    }),
  ]);

  return addApolloState(client, {
    props: {},
  });
};

export default TicketsCheckoutPage;
