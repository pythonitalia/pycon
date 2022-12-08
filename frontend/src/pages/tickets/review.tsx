/** @jsxRuntime classic */

/** @jsx jsx */
import React from "react";
import { FormattedMessage } from "react-intl";
import { Box, Heading, jsx } from "theme-ui";

import { GetStaticProps } from "next";

import { addApolloState, getApolloClient } from "~/apollo/client";
import { CompleteOrder } from "~/components/tickets-page/review/complete-order";
import { HotelRoomsRecap } from "~/components/tickets-page/review/hotel-rooms-recap";
import { InvoiceInformation } from "~/components/tickets-page/review/invoice-information";
import { TicketsRecap } from "~/components/tickets-page/review/tickets-recap";
import { Voucher } from "~/components/tickets-page/review/voucher";
import { HotelRoom, OrderState } from "~/components/tickets-page/types";
import { useCart } from "~/components/tickets-page/use-cart";
import { TicketsPageWrapper } from "~/components/tickets-page/wrapper";
import { prefetchSharedQueries } from "~/helpers/prefetch";
import { TicketItem } from "~/types";

type Props = {
  state: OrderState;
  tickets: TicketItem[];
  hotelRooms: HotelRoom[];
  email: string;
  applyVoucher: (voucher: any) => void;
  removeVoucher: () => void;
};

export const ReviewOrder = ({
  state,
  tickets,
  hotelRooms,
  email,
  applyVoucher,
  removeVoucher,
}: Props) => {
  const { invoiceInformation, selectedProducts, selectedHotelRooms } = state!;

  const productsById = Object.fromEntries(
    tickets!.map((product) => [product.id, product]),
  );

  const hotelRoomsById = Object.fromEntries(
    hotelRooms!.map((room) => [room.id, room]),
  );

  return (
    <Box>
      <Box
        sx={{
          maxWidth: "container",
          mx: "auto",
          px: 3,
          mb: 5,
        }}
      >
        <Heading as="h1">
          <FormattedMessage id="orderReview.heading" />
        </Heading>
      </Box>

      <InvoiceInformation data={invoiceInformation} />

      <TicketsRecap
        selectedProducts={selectedProducts}
        productsById={productsById}
      />

      <HotelRoomsRecap
        selectedHotelRooms={selectedHotelRooms}
        hotelRoomsById={hotelRoomsById}
      />

      <Voucher
        applyVoucher={applyVoucher}
        removeVoucher={removeVoucher}
        state={state}
      />

      <CompleteOrder
        productsById={productsById}
        hotelRoomsById={hotelRoomsById}
        email={email}
        state={state}
      />
    </Box>
  );
};

export const TicketsReviewOrderPage = () => {
  const { state, applyVoucher, removeVoucher } = useCart();

  return (
    <TicketsPageWrapper>
      {({ tickets, me, hotelRooms }) => (
        <ReviewOrder
          email={me && me.email}
          tickets={tickets}
          hotelRooms={hotelRooms}
          state={state}
          applyVoucher={applyVoucher}
          removeVoucher={removeVoucher}
        />
      )}
    </TicketsPageWrapper>
  );
};

export const getStaticProps: GetStaticProps = async ({ locale }) => {
  const client = getApolloClient();

  await Promise.all([prefetchSharedQueries(client, locale)]);

  return addApolloState(client, {
    props: {},
  });
};

export default TicketsReviewOrderPage;
