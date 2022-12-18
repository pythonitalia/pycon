import {
  Grid,
  CardPart,
  MultiplePartsCard,
} from "@python-italia/pycon-styleguide";
import { useEffect } from "react";
import { FormattedMessage } from "react-intl";
import { useFormState } from "react-use-form-state";
import { Select } from "theme-ui";

import { useCountries } from "~/helpers/use-countries";
import { useTranslatedMessage } from "~/helpers/use-translated-message";

import { InputWrapper } from "../input-wrapper";
import { Input, Textarea } from "../inputs";
import { InvoiceInformationState } from "../tickets-page/types";
import { useCart } from "../tickets-page/use-cart";

const FISCAL_CODE_REGEX =
  /^[A-Za-z]{6}[0-9]{2}[A-Za-z]{1}[0-9]{2}[A-Za-z]{1}[0-9]{3}[A-Za-z]{1}$/;

export const BillingCard = () => {
  const {
    state: { invoiceInformation },
    updateInformation,
  } = useCart();

  const invalidFiscalCodeMessage = useTranslatedMessage(
    "orderInformation.invalidFiscalCode",
  );

  const countries = useCountries();
  const [formState, { text, select, textarea }] =
    useFormState<InvoiceInformationState>({ ...invoiceInformation });

  const isBusiness = invoiceInformation.isBusiness;
  const isItalian = formState.values.country === "IT";
  const shouldAskForFiscalCode = !isBusiness && isItalian;

  useEffect(() => updateInformation(formState.values), [formState.values]);

  return (
    <>
      <MultiplePartsCard
        openByDefault={true}
        clickablePart="heading"
        expandTarget="content"
      >
        <CardPart
          title={<FormattedMessage id="tickets.checkout.billing" />}
          contentAlign="left"
          id="heading"
        />
        <CardPart noBg contentAlign="left" id="content">
          <Grid cols={3}>
            {isBusiness && (
              <InputWrapper
                sx={{ mb: 0 }}
                isRequired={true}
                label={<FormattedMessage id="orderInformation.companyName" />}
              >
                <Input {...text("companyName")} required={isBusiness} />
              </InputWrapper>
            )}
            <InputWrapper
              sx={{ mb: 0 }}
              isRequired={true}
              label={<FormattedMessage id="orderInformation.name" />}
            >
              <Input {...text("name")} required={true} />
            </InputWrapper>
            {isBusiness && (
              <InputWrapper
                sx={{ mb: 0 }}
                isRequired={true}
                label={<FormattedMessage id="orderInformation.vatId" />}
              >
                <Input {...text("vatId")} required={true} />
              </InputWrapper>
            )}
            <InputWrapper
              sx={{ mb: 0 }}
              isRequired={true}
              label={<FormattedMessage id="orderInformation.zipCode" />}
            >
              <Input {...text("zipCode")} required={true} />
            </InputWrapper>

            <InputWrapper
              sx={{ mb: 0 }}
              isRequired={true}
              label={<FormattedMessage id="orderInformation.city" />}
            >
              <Input {...text("city")} required={true} />
            </InputWrapper>
            <InputWrapper
              sx={{ mb: 0 }}
              isRequired={true}
              label={<FormattedMessage id="orderInformation.address" />}
            >
              <Textarea rows={3} {...textarea("address")} required={true} />
            </InputWrapper>
            <InputWrapper
              sx={{ mb: 0 }}
              isRequired={true}
              label={<FormattedMessage id="orderInformation.country" />}
            >
              <Select {...select("country")} required={true}>
                {countries.map((c) => (
                  <option key={c.value} value={c.value}>
                    {c.label}
                  </option>
                ))}
              </Select>
            </InputWrapper>

            {shouldAskForFiscalCode && (
              <InputWrapper
                sx={{ mb: 0 }}
                errors={
                  formState.errors.fiscalCode
                    ? [formState.errors.fiscalCode]
                    : null
                }
                isRequired={true}
                label={<FormattedMessage id="orderInformation.fiscalCode" />}
              >
                <Input
                  {...text({
                    name: "fiscalCode",
                    validate: (value) => {
                      const isValid = FISCAL_CODE_REGEX.test(value);

                      if (!isValid) {
                        return invalidFiscalCodeMessage;
                      }
                    },
                    validateOnBlur: true,
                  })}
                  required={true}
                />
              </InputWrapper>
            )}
          </Grid>
        </CardPart>
      </MultiplePartsCard>
    </>
  );
};
