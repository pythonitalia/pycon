import { Section, Heading } from "@python-italia/pycon-styleguide";
import React from "react";
import { FormattedMessage } from "react-intl";

import { GetServerSideProps } from "next";

import { getApolloClient, addApolloState } from "~/apollo/client";
import { Tickets } from "~/components/tickets-page/tickets";
import { TicketsPageWrapper } from "~/components/tickets-page/wrapper";
import { prefetchSharedQueries } from "~/helpers/prefetch";
import { CheckoutCategory, queryTickets } from "~/types";

export const PersonalTicketsPage = ({ cartCookie }) => {
  return (
    <TicketsPageWrapper cartCookie={cartCookie}>
      {({ tickets: products, hotelRooms, conference, me }) => (
        <>
          <Section spacingSize="xl" illustration="snakeTailUp">
            <Heading size="display2">
              <FormattedMessage id="tickets.title" />
            </Heading>
          </Section>

          <Tickets
            products={products}
            hotelRooms={hotelRooms}
            conference={conference}
            me={me}
            business={false}
            visibleCategories={[
              CheckoutCategory.Tickets,
              CheckoutCategory.Hotel,
              CheckoutCategory.Gadgets,
              CheckoutCategory.Membership,
              CheckoutCategory.Tours,
              CheckoutCategory.SocialEvents,
            ]}
            showHeadings={true}
          />
        </>
      )}
    </TicketsPageWrapper>
  );
};

export const getServerSideProps: GetServerSideProps = async ({
  req,
  locale,
}) => {
  const client = getApolloClient(null, req.cookies);

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

  const cartCookie = req.cookies["tickets-cart-v5"];
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

export default PersonalTicketsPage;
