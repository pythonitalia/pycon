/** @jsx jsx */

import { useQuery } from "@apollo/react-hooks";
import {
  Box,
  Button,
  Checkbox,
  Heading,
  Input,
  Select,
  Text,
  Textarea,
} from "@theme-ui/components";
import { ApolloError } from "apollo-client";
import React, { Fragment, useEffect } from "react";
import { FormattedMessage } from "react-intl";
import { useFormState } from "react-use-form-state";
import { Flex, jsx } from "theme-ui";

import { InputWrapper } from "../input-wrapper";
import {
  GENDER_OPTIONS,
  GRANT_TYPE_OPTIONS,
  INTERESTED_IN_VOLUNTEERING_OPTIONS,
  OCCUPATION_OPTIONS,
} from "./options";

export type GrantFormFields = {
  name: string;
  fullName: string;
  email: string;
  age: number;
  gender: string;
  occupation: string;
  grantType: string;
  pythonUsage: string;
  beenToOtherEvents: string;
  interestedInVolunteering: string;
  needsFundsForTravel: boolean;
  why: string;
  notes: string;
  travellingFrom: string;
};

type Props = {};

export const GrantForm: React.SFC<Props> = ({}) => {
  const [
    formState,
    { text, number: numberInput, email, textarea, select, checkbox },
  ] = useFormState<GrantFormFields>(
    {},
    {
      withIds: true,
    },
  );

  const submitGrant = () => {
    console.log(formState.values);
  };

  const getErrors = (key: keyof GrantFormFields) => [""];

  return (
    <Fragment>
      <Text mb={4} as="h1">
        <FormattedMessage id="grants.form.title" />
      </Text>
      <Box as="form" onSubmit={submitGrant}>
        <Heading sx={{ mb: 3 }}>
          <FormattedMessage id="grants.form.aboutYou" />
        </Heading>

        <InputWrapper
          isRequired={true}
          label={<FormattedMessage id="grants.form.fields.fullName" />}
          description={
            <FormattedMessage id="grants.form.fields.fullName.description" />
          }
          errors={getErrors("fullName")}
        >
          <Input {...text("fullName")} required={true} />
        </InputWrapper>

        <InputWrapper
          isRequired={true}
          label={<FormattedMessage id="grants.form.fields.name" />}
          description={
            <FormattedMessage id="grants.form.fields.name.description" />
          }
          errors={getErrors("name")}
        >
          <Input {...text("name")} required={true} />
        </InputWrapper>

        <InputWrapper
          isRequired={true}
          label={<FormattedMessage id="grants.form.fields.email" />}
          description={
            <FormattedMessage id="grants.form.fields.email.description" />
          }
          errors={getErrors("email")}
        >
          <Input {...email("email")} required={true} />
        </InputWrapper>

        <InputWrapper
          isRequired={true}
          errors={getErrors("grantType")}
          label={<FormattedMessage id="grants.form.fields.grantType" />}
        >
          <Select {...select("grantType")} required={true}>
            {GRANT_TYPE_OPTIONS.map(({ value, messageId }) => (
              <FormattedMessage id={messageId} key={messageId}>
                {msg => <option value={value}>{msg}</option>}
              </FormattedMessage>
            ))}
          </Select>
        </InputWrapper>

        <InputWrapper
          isRequired={true}
          label={<FormattedMessage id="grants.form.fields.travellingFrom" />}
          errors={getErrors("travellingFrom")}
        >
          <Input {...text("travellingFrom")} required={true} />
        </InputWrapper>

        <InputWrapper
          errors={getErrors("needsFundsForTravel")}
          label={
            <FormattedMessage id="grants.form.fields.needsFundsForTravel" />
          }
        >
          <Flex>
            <Checkbox {...checkbox("needsFundsForTravel")} />
            <FormattedMessage id="grants.form.fields.needsFundsForTravel.label" />
          </Flex>
        </InputWrapper>

        <InputWrapper
          isRequired={true}
          errors={getErrors("occupation")}
          label={<FormattedMessage id="grants.form.fields.occupation" />}
        >
          <Select {...select("occupation")} required={true}>
            {OCCUPATION_OPTIONS.map(({ value, messageId }) => (
              <FormattedMessage id={messageId} key={messageId}>
                {msg => <option value={value}>{msg}</option>}
              </FormattedMessage>
            ))}
          </Select>
        </InputWrapper>

        <InputWrapper
          isRequired={true}
          errors={getErrors("interestedInVolunteering")}
          label={
            <FormattedMessage id="grants.form.fields.interestedInVolunteering" />
          }
          description={
            <FormattedMessage id="grants.form.fields.interestedInVolunteering.description" />
          }
        >
          <Select {...select("interestedInVolunteering")} required={true}>
            {INTERESTED_IN_VOLUNTEERING_OPTIONS.map(({ value, messageId }) => (
              <FormattedMessage id={messageId} key={messageId}>
                {msg => <option value={value}>{msg}</option>}
              </FormattedMessage>
            ))}
          </Select>
        </InputWrapper>

        <InputWrapper
          isRequired={true}
          label={<FormattedMessage id="grants.form.fields.pythonUsage" />}
          description={
            <FormattedMessage id="grants.form.fields.pythonUsage.description" />
          }
          errors={getErrors("pythonUsage")}
        >
          <Textarea {...textarea("pythonUsage")} required={true} />
        </InputWrapper>

        <InputWrapper
          isRequired={true}
          label={<FormattedMessage id="grants.form.fields.beenToOtherEvents" />}
          errors={getErrors("beenToOtherEvents")}
        >
          <Textarea {...textarea("beenToOtherEvents")} required={true} />
        </InputWrapper>

        <InputWrapper
          isRequired={true}
          label={<FormattedMessage id="grants.form.fields.why" />}
          errors={getErrors("why")}
        >
          <Textarea {...textarea("why")} required={true} />
        </InputWrapper>

        <Box>
          <Heading sx={{ mb: 2 }}>
            <FormattedMessage id="grants.form.optionalInformation" />
          </Heading>

          <Text sx={{ mb: 3 }}>
            <FormattedMessage id="grants.form.optionalInformation.description" />
          </Text>

          <InputWrapper
            label={<FormattedMessage id="grants.form.fields.age" />}
            errors={getErrors("age")}
          >
            <Input {...numberInput("age")} />
          </InputWrapper>

          <InputWrapper
            errors={getErrors("gender")}
            label={<FormattedMessage id="grants.form.fields.gender" />}
          >
            <Select {...select("gender")}>
              {GENDER_OPTIONS.map(({ value, messageId }) => (
                <FormattedMessage id={messageId} key={messageId}>
                  {msg => <option value={value}>{msg}</option>}
                </FormattedMessage>
              ))}
            </Select>
          </InputWrapper>

          <InputWrapper
            label={<FormattedMessage id="grants.form.fields.notes" />}
            errors={getErrors("notes")}
          >
            <Textarea {...textarea("notes")} />
          </InputWrapper>
        </Box>

        <Button>
          <FormattedMessage id="grants.form.submit" />
        </Button>
      </Box>
    </Fragment>
  );
};
