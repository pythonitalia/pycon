/** @jsx jsx */

import { ApolloError, useApolloClient } from "@apollo/client";
import React, { FormEvent, useCallback, useEffect, useState } from "react";
import { FormattedMessage } from "react-intl";
import { useFormState } from "react-use-form-state";
import { Box, Heading, Input, jsx } from "theme-ui";

import { Alert } from "~/components/alert";
import { Button } from "~/components/button/button";
import { GetVoucherDocument, GetVoucherQuery } from "~/types";

import { OrderState, Voucher as VoucherType } from "../types";

type Props = {
  applyVoucher: (voucher: VoucherType) => void;
  removeVoucher: () => void;
  state: OrderState;
};

type VoucherForm = {
  code: string;
};

type QueryStatus = {
  loading: boolean;
  error: ApolloError;
  data: GetVoucherQuery;
};

export const Voucher: React.SFC<Props> = ({
  applyVoucher,
  removeVoucher,
  state,
}) => {
  const conferenceCode = process.env.conferenceCode;
  const apolloClient = useApolloClient();

  const [formState, { text }] = useFormState<VoucherForm>({
    code: state.voucherCode,
  });

  const [{ loading, error, data }, setQueryStatus] = useState<QueryStatus>({
    loading: false,
    error: null,
    data: null,
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

      setQueryStatus({
        loading: true,
        data: null,
        error: null,
      });

      const result = await apolloClient.query<GetVoucherQuery>({
        fetchPolicy: "no-cache",
        query: GetVoucherDocument,
        variables: {
          conference: conferenceCode,
          code: formState.values.code,
        },
      });

      setQueryStatus({
        loading: false,
        data: result.data,
        error: result.error,
      });

      const voucher = result.data.conference.voucher;
      if (voucher) {
        applyVoucher(voucher);
      }
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

        {loading && (
          <Alert variant="info">
            <FormattedMessage id="voucher.loading" />
          </Alert>
        )}

        {error && <Alert variant="alert">{error}</Alert>}

        {data && !data.conference.voucher && (
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
