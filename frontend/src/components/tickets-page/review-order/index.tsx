/** @jsx jsx */
import { RouteComponentProps } from "@reach/router";
import { Box, Heading } from "@theme-ui/components";
import React from "react";
import { FormattedMessage } from "react-intl";
import { jsx } from "theme-ui";

import { HotelRoom } from "../../../generated/graphql-backend";
import { Ticket } from "../../tickets-form/types";
import { OrderState } from "../types";
import { CompleteOrder } from "./complete-order";
import { HotelRoomsRecap } from "./hotel-rooms-recap";
import { InvoiceInformation } from "./invoice-information";
import { TicketsRecap } from "./tickets-recap";
import { Voucher } from "./voucher";

type Props = {
  state: OrderState;
  tickets: Ticket[];
  hotelRooms: HotelRoom[];
  email: string;
} & RouteComponentProps;

export const ReviewOrder: React.SFC<Props> = ({
  state,
  tickets,
  hotelRooms,
  email,
}) => {
  const { invoiceInformation, selectedProducts, selectedHotelRooms } = state!;

  const productsById = Object.fromEntries(
    tickets!.map(product => [product.id, product]),
  );

  const hotelRoomsById = Object.fromEntries(
    hotelRooms!.map(room => [room.id, room]),
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

      <Voucher />

      <CompleteOrder
        productsById={productsById}
        hotelRoomsById={hotelRoomsById}
        email={email}
        state={state}
      />
    </Box>
  );
};
