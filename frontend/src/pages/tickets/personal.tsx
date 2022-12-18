import React from "react";

import { GetStaticProps } from "next";

import { getApolloClient, addApolloState } from "~/apollo/client";
import { Tickets } from "~/components/tickets-page/tickets";
import { TicketsPageWrapper } from "~/components/tickets-page/wrapper";
import { prefetchSharedQueries } from "~/helpers/prefetch";
import { queryTickets } from "~/types";

export const PersonalTicketsPage = () => {
  return (
    <TicketsPageWrapper>
      {({ tickets: products, hotelRooms, conference, me }) => (
        <Tickets
          products={products}
          hotelRooms={hotelRooms}
          conference={conference}
          me={me}
          business={false}
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

export default PersonalTicketsPage;
