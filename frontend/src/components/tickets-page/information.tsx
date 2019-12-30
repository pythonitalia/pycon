/** @jsx jsx */
import {
  Box,
  Button,
  Flex,
  Heading,
  Input,
  Label,
  Radio,
  Select,
  Textarea,
} from "@theme-ui/components";
import React, { useCallback, useEffect } from "react";
import { FormattedMessage } from "react-intl";
import { useFormState } from "react-use-form-state";
import { jsx } from "theme-ui";

import { useCountries } from "../../helpers/use-countries";
import { useTranslatedMessage } from "../../helpers/use-translated-message";
import { InputWrapper } from "../input-wrapper";
import { InvoiceInformationState } from "./types";

type Props = {
  path: string;
  onNextStep: () => void;
  onUpdateInformation: (data: InvoiceInformationState) => void;
  invoiceInformation: InvoiceInformationState;
};

const FISCAL_CODE_REGEX = /^[A-Za-z]{6}[0-9]{2}[A-Za-z]{1}[0-9]{2}[A-Za-z]{1}[0-9]{3}[A-Za-z]{1}$/;

export const InformationSection: React.SFC<Props> = ({
  onNextStep,
  onUpdateInformation,
  invoiceInformation,
}) => {
  const countries = useCountries();
  const invalidFiscalCodeMessage = useTranslatedMessage(
    "orderInformation.invalidFiscalCode",
  );

  const [formState, { text, select, textarea, radio }] = useFormState<
    InvoiceInformationState
  >({ ...invoiceInformation });

  const isBusiness = invoiceInformation.isBusiness;
  const isItalian = formState.values.country === "IT";
  const shouldAskForFiscalCode = !isBusiness && isItalian;

  const onSubmit = useCallback(
    (e: React.MouseEvent<HTMLFormElement>) => {
      e.preventDefault();

      if (shouldAskForFiscalCode && formState.validity.fiscalCode === false) {
        return;
      }

      onNextStep();
    },
    [formState.values],
  );

  useEffect(() => onUpdateInformation(formState.values), [formState.values]);

  return (
    <React.Fragment>
      <Heading as="h1" sx={{ mb: 3 }}>
        <FormattedMessage id="orderInformation.heading" />
      </Heading>

      <Box as="form" onSubmit={onSubmit}>
        {isBusiness && (
          <InputWrapper
            isRequired={true}
            label={<FormattedMessage id="orderInformation.companyName" />}
          >
            <Input {...text("companyName")} required={isBusiness} />
          </InputWrapper>
        )}
        <InputWrapper
          isRequired={true}
          label={<FormattedMessage id="orderInformation.name" />}
        >
          <Input {...text("name")} required={true} />
        </InputWrapper>
        {isBusiness && (
          <InputWrapper
            isRequired={true}
            label={<FormattedMessage id="orderInformation.vatId" />}
          >
            <Input {...text("vatId")} required={true} />
          </InputWrapper>
        )}
        <InputWrapper
          isRequired={true}
          label={<FormattedMessage id="orderInformation.address" />}
        >
          <Textarea {...textarea("address")} required={true} />
        </InputWrapper>
        <InputWrapper
          isRequired={true}
          label={<FormattedMessage id="orderInformation.zipCode" />}
        >
          <Input {...text("zipCode")} required={true} />
        </InputWrapper>
        <InputWrapper
          isRequired={true}
          label={<FormattedMessage id="orderInformation.city" />}
        >
          <Input {...text("city")} required={true} />
        </InputWrapper>
        <InputWrapper
          isRequired={true}
          label={<FormattedMessage id="orderInformation.country" />}
        >
          <Select {...select("country")} required={true}>
            {countries.map(c => (
              <option key={c.value} value={c.value}>
                {c.label}
              </option>
            ))}
          </Select>
        </InputWrapper>

        {shouldAskForFiscalCode && (
          <InputWrapper
            errors={[formState.errors.fiscalCode || ""]}
            isRequired={true}
            label={<FormattedMessage id="orderInformation.fiscalCode" />}
          >
            <Input
              {...text({
                name: "fiscalCode",
                validate: (value, values, e) => {
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

        <Button>
          <FormattedMessage id="order.nextStep" />
        </Button>
      </Box>
    </React.Fragment>
  );
};
