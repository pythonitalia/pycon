/** @jsx jsx */
import React, { FormEvent, useCallback, useEffect } from "react";
import { FormattedMessage } from "react-intl";
import { useFormState } from "react-use-form-state";
import { Box, Heading, Input, jsx } from "theme-ui";

import { Alert } from "~/components/alert";
import { Button } from "~/components/button/button";
import { useGetVoucherMutation } from "~/types";

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

  const [getVoucher, { loading, error, data }] = useGetVoucherMutation({
    onCompleted: (data) => {
      const voucher = data.getConferenceVoucher;
      if (voucher) {
        applyVoucher(voucher);
      }
    },
  });

  const onUseVoucher = useCallback(
    (e?: FormEvent<HTMLFormElement>) => {
      if (e) {
        e.preventDefault();
      }

      if (!formState.values.code) {
        /* what should we do here? remove the current voucher or do nothing? */
        return;
      }

      getVoucher({
        variables: {
          conference: conferenceCode,
          code: formState.values.code,
        },
      });
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

        {data && !data.getConferenceVoucher && (
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
