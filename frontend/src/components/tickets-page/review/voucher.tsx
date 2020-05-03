/** @jsx jsx */
import { Box, Heading, Input } from "@theme-ui/components";
import { GraphQLError } from "graphql";
import React, { FormEvent, useCallback, useEffect, useState } from "react";
import { FormattedMessage } from "react-intl";
import { useFormState } from "react-use-form-state";
import { jsx } from "theme-ui";

import { Alert } from "~/components/alert";
import { Button } from "~/components/button/button";

import { OrderState, Voucher as VoucherType } from "../types";

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
  const conferenceCode = process.env.conferenceCode;

  const [formState, { text }] = useFormState<VoucherForm>({
    code: state.voucherCode,
  });

  const [queryState, setQueryState] = useState<{
    loading: boolean;
    errors?: readonly GraphQLError[];
    // TODO
    data?: any;
  }>({
    loading: false,
    errors: undefined,
    data: undefined,
  });

  const onUseVoucher = useCallback(
    async (e?: FormEvent<HTMLFormElement>) => {
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

      // TODO:
      // const queryData = await apolloClient.query<
      //   GetVoucherQuery,
      //   GetVoucherQueryVariables
      // >({
      //   query: GET_VOUCHER,
      //   fetchPolicy: "network-only",
      //   variables: {
      //     conference: conferenceCode,
      //     code: formState.values.code,
      //   },
      // });

      // setQueryState({
      //   loading: false,
      //   errors: queryData.errors,
      //   data: queryData.errors ? undefined : queryData.data,
      // });

      // const voucher = queryData.data.conference.voucher;

      // if (!voucher) {
      //   /* TODO reset all vouchers? */
      //   return;
      // }

      // applyVoucher(voucher);
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
        <form
          sx={{
            display: "flex",
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
        </form>

        {queryState.loading && (
          <Alert variant="info">
            <FormattedMessage id="voucher.loading" />
          </Alert>
        )}

        {queryState.errors && (
          <Alert variant="alert">
            {queryState.errors.map((e) => e.message).join(",")}
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
