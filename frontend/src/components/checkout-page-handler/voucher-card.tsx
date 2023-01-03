import {
  Text,
  CardPart,
  MultiplePartsCard,
  Spacer,
} from "@python-italia/pycon-styleguide";
import { useMachine } from "@xstate/react";
import { useEffect } from "react";
import { FormattedMessage } from "react-intl";
import { InputElement, useFormState } from "react-use-form-state";

import { useTranslatedMessage } from "~/helpers/use-translated-message";

import { InputWrapper } from "../input-wrapper";
import { Input } from "../inputs";
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

  return (
    <MultiplePartsCard>
      <CardPart
        title={<FormattedMessage id="tickets.checkout.voucher" />}
        contentAlign="left"
      />
      <CardPart noBg contentAlign="left" id="content">
        <InputWrapper
          sx={{ mb: 0 }}
          isRequired
          errors={
            state.matches("notFound")
              ? [<FormattedMessage id="tickets.checkout.voucher.notFound" />]
              : []
          }
        >
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
          />
          {state.matches("fetching") && (
            <>
              <Spacer size="xs" />
              <Text size="label3">
                <FormattedMessage id="tickets.checkout.voucher.fetching" />
              </Text>
            </>
          )}
          {voucherCode && !voucherUsed && (
            <>
              <Spacer size="xs" />
              <Text size="label3">
                <FormattedMessage id="tickets.checkout.voucher.noProductsAffected" />
              </Text>
            </>
          )}
        </InputWrapper>
      </CardPart>
    </MultiplePartsCard>
  );
};
