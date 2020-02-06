/** @jsx jsx */
import { Box, Button, Flex, Heading, Input, Text } from "@theme-ui/components";
import React, { Fragment, useCallback, useContext } from "react";
import { FormattedMessage } from "react-intl";
import { useFormState } from "react-use-form-state";
import { jsx } from "theme-ui";

import { useCurrentLanguage } from "../../../context/language";
import { HotelRoom } from "../../../generated/graphql-backend";
import { Link } from "../../link";
import { Ticket } from "../../tickets-form/types";
import { OrderState, SelectedHotelRooms } from "../types";
import { CreateOrderButtons } from "./create-order-buttons";
import { ReviewItem } from "./review-item";

type Props = {
  email: string;
  state: OrderState;
  hotelRoomsById: {
    [x: string]: HotelRoom;
    [x: number]: HotelRoom;
  };
  productsById: {
    [x: string]: Ticket;
    [x: number]: Ticket;
  };
};

type VoucherForm = {
  code: string;
};

const calculateTotalAmount = (
  state: OrderState,
  productsById: {
    [x: string]: Ticket;
    [x: number]: Ticket;
  },
  hotelRoomsById: {
    [x: string]: HotelRoom;
    [x: number]: HotelRoom;
  },
) => {
  const ticketsPrice = Object.values(state.selectedProducts)
    .flat()
    .reduce((p, c) => p + parseFloat(productsById[c.id].defaultPrice), 0);
  const hotelRoomsPrice = Object.values(state.selectedHotelRooms)
    .flat()
    .reduce(
      (p, c) => p + parseFloat(hotelRoomsById[c.id].price) * c.numNights,
      0,
    );
  return ticketsPrice + hotelRoomsPrice;
};

export const CompleteOrder: React.SFC<Props> = ({
  email,
  state,
  productsById,
  hotelRoomsById,
}) => {
  const totalAmount = calculateTotalAmount(state, productsById, hotelRoomsById);
  const [formState, { text }] = useFormState<VoucherForm>();

  return (
    <Box sx={{ py: 5, borderTop: "primary" }}>
      <Box
        sx={{
          maxWidth: "container",
          mx: "auto",
          px: 3,
        }}
      >
        <Heading
          as="h2"
          sx={{
            color: "orange",
            textTransform: "uppercase",
            mb: 4,
            fontWeight: "bold",
          }}
        >
          <FormattedMessage id="orderReview.total" />
        </Heading>

        <Box
          sx={{
            maxWidth: "660px",
            borderTop: "primary",
            borderBottom: "primary",
            mt: 4,
            py: 3,
          }}
        >
          <Text
            sx={{
              fontSize: 4,
              fontWeight: "bold",
            }}
          >
            <FormattedMessage
              id="orderReview.totalAmount"
              values={{
                total: totalAmount,
              }}
            />
          </Text>
        </Box>

        <CreateOrderButtons email={email} state={state} />
      </Box>
    </Box>
  );
};
