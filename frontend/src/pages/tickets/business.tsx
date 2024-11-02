import { Heading, Section } from "@python-italia/pycon-styleguide";
import React from "react";
import { FormattedMessage } from "react-intl";

import type { GetServerSideProps } from "next";

import { addApolloState, getApolloClient } from "~/apollo/client";
import { Tickets } from "~/components/tickets-page/tickets";
import { TicketsPageWrapper } from "~/components/tickets-page/wrapper";
import { prefetchSharedQueries } from "~/helpers/prefetch";
import { CheckoutCategory, queryCurrentUser, queryTickets } from "~/types";

export const BusinessTicketsPage = ({ cartCookie }) => {
  return (
    <TicketsPageWrapper cartCookie={cartCookie}>
      {({ tickets: products, conference, me }) => (
        <>
          <Section spacingSize="xl" illustration="snakeTailUp">
            <Heading size="display2">
              <FormattedMessage id="tickets.title" />
            </Heading>
          </Section>

          <Tickets
            products={products}
            conference={conference}
            me={me}
            business={true}
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

  try {
    await queryCurrentUser(client, {
      conference: process.env.conferenceCode,
    });
  } catch (e) {
    console.debug("User not logged in");
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

export default BusinessTicketsPage;
