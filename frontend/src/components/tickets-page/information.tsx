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
import { InputWrapper } from "../input-wrapper";
import { ReviewItem } from "./review-item";
import { InvoiceInformationState } from "./types";

type Props = {
  path: string;
  onNextStep: () => void;
  onUpdateInformation: (data: InvoiceInformationState) => void;
  invoiceInformation: InvoiceInformationState;
};

export const InformationSection: React.SFC<Props> = ({
  onNextStep,
  onUpdateInformation,
  invoiceInformation,
}) => {
  const countries = useCountries();

  const [formState, { text, select, textarea, radio }] = useFormState<
    InvoiceInformationState
  >({ ...invoiceInformation });

  const onSubmit = useCallback(
    (e: React.MouseEvent<HTMLFormElement>) => {
      e.preventDefault();
      onNextStep();
    },
    [formState.values],
  );

  useEffect(() => onUpdateInformation(formState.values), [formState.values]);

  const isBusiness = invoiceInformation.isBusiness;
  const isItalian = formState.values.country === "IT";

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

        {!isBusiness && isItalian && (
          <InputWrapper
            isRequired={true}
            label={<FormattedMessage id="orderInformation.fiscalCode" />}
          >
            <Input {...text("fiscalCode")} required={true} />
          </InputWrapper>
        )}

        <Button>
          <FormattedMessage id="order.nextStep" />
        </Button>
      </Box>
    </React.Fragment>
  );
};
