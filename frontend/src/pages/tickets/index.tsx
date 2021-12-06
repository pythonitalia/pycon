/** @jsxRuntime classic */

/** @jsx jsx */
import { jsx } from "theme-ui";

import { GetStaticPaths, GetStaticProps } from "next";
import { useRouter } from "next/router";

import { addApolloState, getApolloClient } from "~/apollo/client";
import { useLoginState } from "~/components/profile/hooks";
import { TicketsSection } from "~/components/tickets-page/tickets-section";
import { useCart } from "~/components/tickets-page/use-cart";
import { TicketsPageWrapper } from "~/components/tickets-page/wrapper";
import { prefetchSharedQueries } from "~/helpers/prefetch";
import { useCurrentLanguage } from "~/locale/context";
import { queryTickets } from "~/types";

export const TicketsPage = () => {
  const language = useCurrentLanguage();
  const [isLoggedIn] = useLoginState();

  const router = useRouter();

  const {
    state,
    addHotelRoom,
    addProduct,
    removeProduct,
    removeHotelRoom,
    updateIsBusiness,
  } = useCart();

  return (
    <TicketsPageWrapper>
      {({ tickets, hotelRooms, conference }) => (
        <TicketsSection
          state={state}
          conferenceStart={conference.start}
          conferenceEnd={conference.end}
          hotelRooms={hotelRooms}
          selectedHotelRooms={state.selectedHotelRooms}
          tickets={tickets}
          selectedProducts={state.selectedProducts}
          addProduct={addProduct}
          removeProduct={removeProduct}
          addHotelRoom={addHotelRoom}
          removeHotelRoom={removeHotelRoom}
          invoiceInformation={state.invoiceInformation}
          onUpdateIsBusiness={updateIsBusiness}
          onNextStep={() => {
            const nextUrl = `/tickets/information/`;

            if (isLoggedIn) {
              router.push("/tickets/information/", nextUrl);
            } else {
              router.push(`/login?next=${nextUrl}`);
            }
          }}
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
      language: locale,
      isLogged: false,
    }),
  ]);

  return addApolloState(client, {
    props: {},
  });
};

export default TicketsPage;
