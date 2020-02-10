/** @jsx jsx */
import { useLazyQuery, useApolloClient, useQuery } from "@apollo/react-hooks";
import { Box, Button, Flex, Heading, Input, Text } from "@theme-ui/components";
import React, {
  Fragment,
  useCallback,
  useContext,
  useEffect,
  useState,
} from "react";
import { FormattedMessage } from "react-intl";
import { useFormState } from "react-use-form-state";
import { jsx } from "theme-ui";

import { useConference } from "../../../context/conference";
import { useCurrentLanguage } from "../../../context/language";
import {
  GetVoucherQuery,
  GetVoucherQueryVariables,
  Voucher as VoucherType,
} from "../../../generated/graphql-backend";
import { Link } from "../../link";
import { Ticket } from "../../tickets-form/types";
import { OrderState, SelectedHotelRooms } from "../types";
import { CreateOrderButtons } from "./create-order-buttons";
import GET_VOUCHER from "./get-voucher.graphql";
import { ReviewItem } from "./review-item";
import { GraphQLError } from "graphql";
import { Alert } from "../../alert";

type Props = {
  applyVoucher: (voucher: VoucherType) => void;
  removeVoucher: () => void;
  state: OrderState;
};

type VoucherForm = {
  code: string;
};

export const Voucher: React.SFC<Props> = ({
  applyVoucher,
  removeVoucher,
  state,
}) => {
  const { code: conferenceCode } = useConference();
  const apolloClient = useApolloClient();

  const [formState, { text }] = useFormState<VoucherForm>({
    code: state.voucherCode,
  });

  const [queryState, setQueryState] = useState<{
    loading: boolean;
    errors?: readonly GraphQLError[];
    data?: GetVoucherQuery;
  }>({
    loading: false,
    errors: undefined,
    data: undefined,
  });

  const onUseVoucher = useCallback(
    async (e?: React.MouseEvent) => {
      if (e) {
        e.preventDefault();
      }

      if (!formState.values.code) {
        /* what should we do here? remove the current voucher or do nothing? */
        return;
      }

      setQueryState({
        loading: true,
        errors: undefined,
        data: undefined,
      });

      const queryData = await apolloClient.query<
        GetVoucherQuery,
        GetVoucherQueryVariables
      >({
        query: GET_VOUCHER,
        fetchPolicy: "network-only",
        variables: {
          conference: conferenceCode,
          code: formState.values.code,
        },
      });

      setQueryState({
        loading: false,
        errors: queryData.errors,
        data: queryData.errors ? undefined : queryData.data,
      });

      const voucher = queryData.data.conference.voucher;

      if (!voucher) {
        /* TODO reset all vouchers? */
        return;
      }

      applyVoucher(voucher);
    },
    [formState.values],
  );

  useEffect(() => {
    // TODO: maybe we want to move this in tickets-page/index.tsx?
    // It feels a bit dirty to mix UI and side effects (= reloading the voucher)

    if (formState.values.code) {
      onUseVoucher();
    }
  }, []);

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
          <FormattedMessage id="voucher.voucherHeading" />
        </Heading>
        <Flex
          as="form"
          sx={{
            flexDirection: ["column", "column", "row"],
            mb: 4,
          }}
          onSubmit={onUseVoucher}
        >
          <Input
            sx={{
              maxWidth: ["none", "none", "300px"],
              mr: 2,
            }}
            {...text("code")}
            required={true}
          />
          <Button
            sx={{
              textTransform: "uppercase",
              mt: [2, 2, 0],
            }}
          >
            <FormattedMessage id="voucher.redeemVoucher" />
          </Button>
          {state.voucherCode && (
            <Button
              sx={{
                textTransform: "uppercase",
                ml: [0, 0, 2],
                mt: [2, 2, 0],
              }}
              onClick={removeVoucher}
            >
              <FormattedMessage
                id="voucher.removeVoucher"
                values={{
                  code: state.voucherCode,
                }}
              />
            </Button>
          )}
        </Flex>

        {queryState.loading && (
          <Alert variant="info">
            <FormattedMessage id="voucher.loading" />
          </Alert>
        )}

        {queryState.errors && (
          <Alert variant="alert">
            {queryState.errors.map(e => e.message).join(",")}
          </Alert>
        )}

        {queryState.data && !queryState.data.conference.voucher && (
          <Alert variant="alert">
            <FormattedMessage id="voucher.codeNotValid" />
          </Alert>
        )}

        {state.voucherCode && !state.voucherUsed && (
          <Alert variant="info">
            <FormattedMessage id="voucher.noProductsAffected" />
          </Alert>
        )}
      </Box>
    </Box>
  );
};
