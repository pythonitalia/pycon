
/** @jsx jsx */

import { useRouter } from "next/router";
import { jsx } from "theme-ui";

import { useLoginState } from "~/app/profile/hooks";
import { TicketsSection } from "~/components/tickets-page/tickets-section";
import { useCart } from "~/components/tickets-page/use-cart";
import { TicketsPageWrapper } from "~/components/tickets-page/wrapper";
import { useCurrentLanguage } from "~/locale/context";

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

export default TicketsPage;
