/** @jsx jsx */
import { useLazyQuery } from "@apollo/react-hooks";
import { Box, Button, Flex, Heading, Input, Text } from "@theme-ui/components";
import React, { Fragment, useCallback, useContext } from "react";
import { FormattedMessage } from "react-intl";
import { useFormState } from "react-use-form-state";
import { jsx } from "theme-ui";

import { useConference } from "../../../context/conference";
import { useCurrentLanguage } from "../../../context/language";
import {
  GetVoucherQuery,
  GetVoucherQueryVariables,
  HotelRoom,
} from "../../../generated/graphql-backend";
import { Link } from "../../link";
import { Ticket } from "../../tickets-form/types";
import { OrderState, SelectedHotelRooms } from "../types";
import { CreateOrderButtons } from "./create-order-buttons";
import GET_VOUCHER from "./get-voucher.graphql";
import { ReviewItem } from "./review-item";

type Props = {};

type VoucherForm = {
  code: string;
};

export const Voucher: React.SFC<Props> = ({}) => {
  const { code: conferenceCode } = useConference();

  const [formState, { text }] = useFormState<VoucherForm>();
  const [getVoucher, { loading, error }] = useLazyQuery<
    GetVoucherQuery,
    GetVoucherQueryVariables
  >(GET_VOUCHER);

  const onUseVoucher = useCallback(
    async (e: React.MouseEvent) => {
      e.preventDefault();

      if (!formState.validity.code) {
        return;
      }

      const voucher = await getVoucher({
        variables: {
          conference: conferenceCode,
          code: formState.values.code,
        },
      });
    },
    [formState.values],
  );

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
          onSubmit={onUseVoucher}
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
