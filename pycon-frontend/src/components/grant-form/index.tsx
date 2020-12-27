/** @jsxRuntime classic */
/** @jsx jsx */
import React, { Fragment, useCallback } from "react";
import { FormattedMessage } from "react-intl";
import { useFormState } from "react-use-form-state";
import {
  Box,
  Checkbox,
  Flex,
  Heading,
  Input,
  jsx,
  Select,
  Text,
  Textarea,
} from "theme-ui";

import { useSendGrantRequestMutation } from "~/types";

import { Alert } from "../alert";
import { Button } from "../button/button";
import { ErrorsList } from "../errors-list";
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

type Props = { conference: string };

export const GrantForm: React.SFC<Props> = ({ conference }) => {
  const [
    formState,
    { text, number: numberInput, email, textarea, select, checkbox },
  ] = useFormState<GrantFormFields>(
    {},
    {
      withIds: true,
    },
  );

  const [submitGrant, { loading, data }] = useSendGrantRequestMutation();

  const onSubmit = useCallback(
    (e) => {
      e.preventDefault();
      submitGrant({
        variables: {
          input: {
            conference,
            age: +formState.values.age,
            fullName: formState.values.fullName,
            name: formState.values.name,
            gender: formState.values.gender,
            beenToOtherEvents: formState.values.beenToOtherEvents,
            interestedInVolunteering: formState.values.interestedInVolunteering,
            notes: formState.values.notes,
            grantType: formState.values.grantType,
            needsFundsForTravel: formState.values.needsFundsForTravel,
            why: formState.values.why,
            travellingFrom: formState.values.travellingFrom,
            email: formState.values.email,
            occupation: formState.values.occupation,
            pythonUsage: formState.values.pythonUsage,
          },
        },
      });
    },
    [formState.values],
  );

  const getErrors = (
    key: keyof GrantFormFields | "nonFieldErrors",
  ): string[] => {
    if (data?.sendGrantRequest.__typename === "SendGrantRequestErrors") {
      let errorKey: string = key;

      if (key !== "nonFieldErrors") {
        const capitalized = key.charAt(0).toUpperCase() + key.slice(1);
        errorKey = `validation${capitalized}`;
      }

      return (data.sendGrantRequest as any)[errorKey];
    }

    return [];
  };

  if (!loading && data?.sendGrantRequest.__typename === "GrantRequest") {
    return (
      <Text>
        <FormattedMessage id="grants.form.sent" />
      </Text>
    );
  }

  return (
    <Fragment>
      <Text mb={4} as="h1">
        <FormattedMessage id="grants.form.title" />
      </Text>
      <Box as="form" onSubmit={onSubmit}>
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
                {(msg) => <option value={value}>{msg}</option>}
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
                {(msg) => <option value={value}>{msg}</option>}
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
                {(msg) => <option value={value}>{msg}</option>}
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
                  {(msg) => <option value={value}>{msg}</option>}
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

        <ErrorsList sx={{ mb: 3 }} errors={getErrors("nonFieldErrors")} />

        {loading && (
          <Alert
            sx={{
              mb: 3,
            }}
            variant="info"
          >
            <FormattedMessage id="grants.form.sendingRequest" />
          </Alert>
        )}

        <Button loading={loading}>
          <FormattedMessage id="grants.form.submit" />
        </Button>
      </Box>
    </Fragment>
  );
};
