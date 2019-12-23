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
import React, { useEffect } from "react";
import { useFormState } from "react-use-form-state";
import { jsx } from "theme-ui";

import { useCountries } from "../../helpers/use-countries";
import { InputWrapper } from "../input-wrapper";
import { InvoiceInformationState } from "./types";

type Props = {
  path: string;
  onNextStep: () => void;
  onUpdateInformation: (data: InvoiceInformationState) => void;
};

export const InformationSection: React.SFC<Props> = ({
  onNextStep,
  onUpdateInformation,
}) => {
  const countries = useCountries();

  const [formState, { text, select, textarea, radio }] = useFormState<
    InvoiceInformationState
  >({ isBusiness: "false" });

  const isBusiness = formState.values.isBusiness === "true";

  useEffect(() => onUpdateInformation(formState.values), [formState.values]);

  return (
    <React.Fragment>
      <Heading sx={{ mb: 3 }}>Invoice information</Heading>

      <Box>
        <Flex mb={3} sx={{ display: ["block", "flex"] }}>
          <Label
            sx={{
              width: "auto",
              mr: 3,
              mb: [3, 0],
              color: "green",
              fontWeight: "bold",
            }}
          >
            <Radio {...radio("isBusiness", "false")} /> Individual Customer
          </Label>
          <Label
            sx={{
              width: "auto",
              mr: 3,
              color: "green",
              fontWeight: "bold",
            }}
          >
            <Radio {...radio("isBusiness", "true")} /> Business Customer
          </Label>
        </Flex>
        {isBusiness && (
          <InputWrapper label="Company name">
            <Input {...text("companyName")} required={isBusiness} />
          </InputWrapper>
        )}
        <InputWrapper label="Name">
          <Input {...text("name")} required={true} />
        </InputWrapper>
        <InputWrapper label="VAT ID">
          <Input {...text("vatId")} required={true} />
        </InputWrapper>
        <InputWrapper label="Address">
          <Textarea {...textarea("address")} required={true} />
        </InputWrapper>
        <InputWrapper label="Zip Code">
          <Input {...text("zipCode")} required={true} />
        </InputWrapper>
        <InputWrapper label="City">
          <Input {...text("city")} required={true} />
        </InputWrapper>
        <InputWrapper label="Country">
          <Select {...select("country")} required={true}>
            {countries.map(c => (
              <option key={c.value} value={c.value}>
                {c.label}
              </option>
            ))}
          </Select>
        </InputWrapper>
      </Box>

      <Button onClick={onNextStep}>Next step</Button>
    </React.Fragment>
  );
};
