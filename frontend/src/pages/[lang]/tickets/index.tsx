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
            const nextUrl = `/${language}/tickets/information/`;

            if (isLoggedIn) {
              router.push("/[lang]/tickets/information/", nextUrl);
            } else {
              router.push(
                `/[lang]/login?next=${nextUrl}`,
                `/${language}/login?next=${nextUrl}`,
              );
            }
          }}
        />
      )}
    </TicketsPageWrapper>
  );
};

// export const getStaticProps: GetStaticProps = async ({ params }) => {
//   const language = params.lang as string;
//   const client = getApolloClient();

//   await Promise.all([
//     prefetchSharedQueries(client, language),
//     queryTickets(client, {
//       conference: process.env.conferenceCode,
//       language,
//       isLogged: false,
//     }),
//   ]);

//   return addApolloState(client, {
//     props: {},
//   });
// };

// export const getStaticPaths: GetStaticPaths = async () =>
//   Promise.resolve({
//     paths: [],
//     fallback: "blocking",
//   });

export default TicketsPage;
