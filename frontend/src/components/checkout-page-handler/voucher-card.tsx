import {
  CardPart,
  Heading,
  Input,
  InputWrapper,
  MultiplePartsCard,
  Text,
} from "@python-italia/pycon-styleguide";
import { useMachine } from "@xstate/react";
import { useEffect } from "react";
import { FormattedMessage } from "react-intl";
import { InputElement, useFormState } from "react-use-form-state";

import { useTranslatedMessage } from "~/helpers/use-translated-message";

import { useCart } from "../tickets-page/use-cart";
import { voucherMachine } from "./voucher-machine";

type VoucherForm = {
  code: string;
};

export const VoucherCard = () => {
  const {
    state: { voucherCode, voucherUsed },
    applyVoucher,
    removeVoucher,
  } = useCart();

  const [_, { text }] = useFormState<VoucherForm>({
    code: voucherCode,
  });

  const [state, send] = useMachine(voucherMachine, {
    actions: {
      applyVoucher: (context) => {
        applyVoucher(context.voucher);
      },
      removeVoucher: () => {
        removeVoucher();
      },
    },
  });

  useEffect(() => {
    if (voucherCode) {
      send({
        type: "changeCode",
        value: voucherCode,
      });
    }
  }, []);

  const voucherPlaceholder = useTranslatedMessage(
    "tickets.checkout.voucher.placeholder",
  );

  const voucherNotFound = useTranslatedMessage(
    "tickets.checkout.voucher.notFound",
  );

  return (
    <MultiplePartsCard>
      <CardPart contentAlign="left">
        <Heading size={2}>
          <FormattedMessage id="tickets.checkout.voucher" />
        </Heading>
      </CardPart>
      <CardPart background="milk" contentAlign="left" id="content">
        <InputWrapper required>
          <Input
            {...text({
              name: "code",
              onChange: (e: React.ChangeEvent<InputElement>) => {
                send({
                  type: "changeCode",
                  value: e.target.value,
                });
              },
            })}
            placeholder={voucherPlaceholder}
            errors={state.matches("notFound") ? [voucherNotFound] : []}
          />
          {state.matches("fetching") && (
            <Text size="label4">
              <FormattedMessage id="tickets.checkout.voucher.fetching" />
            </Text>
          )}
          {voucherCode && !voucherUsed && (
            <Text size="label4">
              <FormattedMessage id="tickets.checkout.voucher.noProductsAffected" />
            </Text>
          )}
        </InputWrapper>
      </CardPart>
    </MultiplePartsCard>
  );
};
