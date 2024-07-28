import {
  CardPart,
  Checkbox,
  Grid,
  GridColumn,
  Heading,
  HorizontalStack,
  Input,
  InputWrapper,
  MultiplePartsCard,
  Select,
  Spacer,
  Text,
  Textarea,
} from "@python-italia/pycon-styleguide";
import { useEffect } from "react";
import { FormattedMessage } from "react-intl";
import { useFormState } from "react-use-form-state";

import { useCountries } from "~/helpers/use-countries";
import { useTranslatedMessage } from "~/helpers/use-translated-message";

import type { CurrentUserQueryResult } from "~/types";
import type { InvoiceInformationState } from "../tickets-page/types";
import { useCart } from "../tickets-page/use-cart";

const FISCAL_CODE_REGEX =
  /^[A-Za-z]{6}[0-9]{2}[A-Za-z]{1}[0-9]{2}[A-Za-z]{1}[0-9]{3}[A-Za-z]{1}$/;

export const BillingCard = ({
  me,
}: {
  me: CurrentUserQueryResult["data"]["me"];
}) => {
  const {
    state: { invoiceInformation, hasAdmissionTicket },
    updateInformation,
  } = useCart();
  const savedBillingInformation = me?.billingAddresses.find(
    (billingAddress) =>
      billingAddress.isBusiness === invoiceInformation.isBusiness,
  );

  const invalidFiscalCodeMessage = useTranslatedMessage(
    "orderInformation.invalidFiscalCode",
  );
  const invalidSDIMessage = useTranslatedMessage("orderInformation.invalidSDI");

  const countries = useCountries();
  const [formState, { text, email, select, textarea, checkbox }] =
    useFormState<InvoiceInformationState>({ ...invoiceInformation });

  const isBusiness = invoiceInformation.isBusiness;
  const isItalian = formState.values.country === "IT";

  const inputPlaceholder = useTranslatedMessage("input.placeholder");

  useEffect(() => {
    const emptyInvoiceInformation = Object.entries(invoiceInformation).every(
      ([key, value]) => key === "isBusiness" || !value,
    );
    if (emptyInvoiceInformation && savedBillingInformation) {
      formState.setField("companyName", savedBillingInformation.companyName);
      formState.setField("name", savedBillingInformation.userName);
      formState.setField("fiscalCode", savedBillingInformation.fiscalCode);
      formState.setField("pec", savedBillingInformation.pec);
      formState.setField("sdi", savedBillingInformation.sdi);
      formState.setField("vatId", savedBillingInformation.vatId);
      formState.setField("address", savedBillingInformation.address);
      formState.setField("zipCode", savedBillingInformation.zipCode);
      formState.setField("city", savedBillingInformation.city);
      formState.setField("country", savedBillingInformation.country);

      updateInformation(formState.values);
    }
  }, []);

  useEffect(() => {
    if (invoiceInformation.isBusiness && !formState.values.isBusiness) {
      formState.setField("companyName", "");
      formState.setField("vatId", "");
    }
    updateInformation(formState.values);
  }, [formState.values]);

  return (
    <>
      <MultiplePartsCard
        openByDefault={true}
        clickablePart="heading"
        expandTarget="content"
      >
        <CardPart contentAlign="left" id="heading">
          <Heading size={2}>
            <FormattedMessage id="tickets.checkout.billing" />
          </Heading>
        </CardPart>
        <CardPart background="milk" contentAlign="left" id="content">
          <Grid cols={3}>
            {!hasAdmissionTicket && (
              <GridColumn colSpan={3}>
                <InputWrapper
                  title={
                    <FormattedMessage id="checkout.billing.businessInvoice" />
                  }
                >
                  <HorizontalStack
                    wrap="wrap"
                    gap="small"
                    alignItems="center"
                    justifyContent="spaceBetween"
                  >
                    <Text size={2}>
                      <FormattedMessage id="checkout.billing.businessInvoice.description" />
                    </Text>
                    <Checkbox {...checkbox("isBusiness")} />
                  </HorizontalStack>
                </InputWrapper>
              </GridColumn>
            )}
            {isBusiness && (
              <InputWrapper
                required={true}
                title={<FormattedMessage id="orderInformation.companyName" />}
              >
                <Input
                  {...text("companyName")}
                  autoComplete="organization"
                  required={isBusiness}
                  placeholder={inputPlaceholder}
                />
              </InputWrapper>
            )}
            <InputWrapper
              required={true}
              title={<FormattedMessage id="orderInformation.name" />}
            >
              <Input
                {...text("name")}
                required={true}
                placeholder={inputPlaceholder}
              />
            </InputWrapper>
            {isBusiness && (
              <InputWrapper
                required={true}
                title={<FormattedMessage id="orderInformation.vatId" />}
              >
                <Input
                  {...text("vatId")}
                  autoComplete="off"
                  required={true}
                  placeholder={inputPlaceholder}
                />
              </InputWrapper>
            )}
            <InputWrapper
              required={true}
              title={<FormattedMessage id="orderInformation.zipCode" />}
            >
              <Input
                {...text("zipCode")}
                required={true}
                placeholder={inputPlaceholder}
              />
            </InputWrapper>

            <InputWrapper
              required={true}
              title={<FormattedMessage id="orderInformation.city" />}
            >
              <Input
                {...text("city")}
                required={true}
                placeholder={inputPlaceholder}
              />
            </InputWrapper>
            <InputWrapper
              required={true}
              title={<FormattedMessage id="orderInformation.address" />}
            >
              <Textarea
                rows={3}
                {...textarea("address")}
                autoComplete="street-address"
                required={true}
                placeholder={inputPlaceholder}
              />
            </InputWrapper>
            <InputWrapper
              required={true}
              title={<FormattedMessage id="orderInformation.country" />}
            >
              <Select {...select("country")} required={true}>
                <FormattedMessage id="input.selectCountryPlaceholder">
                  {(msg) => (
                    <option value="" disabled>
                      {msg}
                    </option>
                  )}
                </FormattedMessage>
                {countries.map((c) => (
                  <option key={c.value} value={c.value}>
                    {c.label}
                  </option>
                ))}
              </Select>
            </InputWrapper>
          </Grid>

          {isItalian && (
            <>
              <Spacer size="medium" />
              <Heading size={3}>
                <FormattedMessage id="orderInformation.italianInvoice" />
              </Heading>
              <Spacer size="medium" />

              <Grid cols={3}>
                {isBusiness ? (
                  <InputWrapper
                    required={true}
                    title={<FormattedMessage id="orderInformation.sdi" />}
                  >
                    <Input
                      {...text({
                        name: "sdi",
                        validate: (value) => {
                          const isValid = value.length === 7;

                          if (!isValid) {
                            return invalidSDIMessage;
                          }
                        },
                        validateOnBlur: true,
                      })}
                      required={true}
                      errors={
                        formState.errors.sdi ? [formState.errors.sdi] : null
                      }
                    />
                  </InputWrapper>
                ) : (
                  <InputWrapper
                    required={true}
                    title={
                      <FormattedMessage id="orderInformation.fiscalCode" />
                    }
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
                      errors={
                        formState.errors.fiscalCode
                          ? [formState.errors.fiscalCode]
                          : null
                      }
                    />
                  </InputWrapper>
                )}
                <InputWrapper
                  title={<FormattedMessage id="orderInformation.pec" />}
                >
                  <Input
                    {...email({
                      name: "pec",
                    })}
                    errors={
                      formState.errors.pec ? [formState.errors.pec] : null
                    }
                  />
                </InputWrapper>
              </Grid>
            </>
          )}
        </CardPart>
      </MultiplePartsCard>
    </>
  );
};
