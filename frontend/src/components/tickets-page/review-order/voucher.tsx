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

type Props = {};

type VoucherForm = {
  code: string;
};

export const Voucher: React.SFC<Props> = ({}) => {
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
          Voucher
        </Heading>
        <Flex
          as="form"
          sx={{
            mb: 4,
          }}
        >
          <Input
            sx={{
              maxWidth: "300px",
              mr: 2,
            }}
            {...text("code")}
            required={true}
          />
          <Button>Redeem</Button>
        </Flex>
      </Box>
    </Box>
  );
};
