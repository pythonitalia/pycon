import React from "react";

import { GetServerSideProps } from "next";

import { addApolloState, getApolloClient } from "~/apollo/client";
import { CheckoutPageHandler } from "~/components/checkout-page-handler";
import { TicketsPageWrapper } from "~/components/tickets-page/wrapper";
import { prefetchSharedQueries } from "~/helpers/prefetch";
import { queryCurrentUser, queryTickets } from "~/types";

export const TicketsCheckoutPage = ({ cartCookie }) => {
  return (
    <TicketsPageWrapper cartCookie={cartCookie}>
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

export const getServerSideProps: GetServerSideProps = async ({
  req,
  locale,
}) => {
  const identityToken = req.cookies["pythonitalia_sessionid"];
  if (!identityToken) {
    return {
      redirect: {
        destination: "/login",
        permanent: false,
      },
    };
  }

  const client = getApolloClient(null, req.cookies);

  try {
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
      queryCurrentUser(client),
    ]);
  } catch (e) {
    return {
      redirect: {
        destination: "/login",
        permanent: false,
      },
    };
  }

  const cartCookie = req.cookies["tickets-cart-v6"];
  return addApolloState(
    client,
    {
      props: {
        cartCookie,
      },
    },
    null,
  );
};

export default TicketsCheckoutPage;
