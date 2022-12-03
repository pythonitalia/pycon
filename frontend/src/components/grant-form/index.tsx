/** @jsxRuntime classic */

/** @jsx jsx */
import React, { Fragment, useCallback, useEffect } from "react";
import { FormattedMessage } from "react-intl";
import { useFormState } from "react-use-form-state";
import {
  Box,
  Checkbox,
  Heading,
  Input,
  Label,
  jsx,
  Select,
  Text,
  Textarea,
} from "theme-ui";

import { useCurrentUser } from "~/helpers/use-current-user";
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
  AGE_GROUPS_OPTIONS,
} from "./options";

export type GrantFormFields = {
  name: string;
  fullName: string;
  ageGroup: string;
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

export const GrantForm = ({ conference }: Props) => {
  const { user, loading: loadingUser } = useCurrentUser({});
  const [formState, { text, textarea, select, checkbox }] = useFormState<
    GrantFormFields
  >(
    {},
    {
      withIds: true,
    },
  );

  useEffect(() => {
    if (user) {
      formState.setField("fullName", user.fullName);
      formState.setField("name", user.name);
      formState.setField("gender", user.gender);
      // if (user.dateBirth) {
      //   formState.setField(
      //     "age",
      //     new Date().getFullYear() - new Date(user.dateBirth).getFullYear(),
      //   );
      // }
    }
  }, [user]);

  const [submitGrant, { loading, data }] = useSendGrantRequestMutation();

  const onSubmit = useCallback(
    (e) => {
      e.preventDefault();
      submitGrant({
        variables: {
          input: {
            conference,
            ageGroup: formState.values.ageGroup,
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

  if (loadingUser) {
    return (
      <Alert variant="info">
        <FormattedMessage id="global.loading" />
      </Alert>
    );
  }

  return (
    <Fragment>
      <Heading mb={4} as="h1">
        <FormattedMessage id="grants.form.title" />
      </Heading>
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
          errors={getErrors("grantType")}
          label={<FormattedMessage id="grants.form.fields.grantType" />}
        >
          <Select {...select("grantType")} required={true}>
            {GRANT_TYPE_OPTIONS.map(({ value, disabled, messageId }) => (
              <FormattedMessage id={messageId} key={messageId}>
                {(msg) => (
                  <option disabled={disabled} value={value}>
                    {msg}
                  </option>
                )}
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
          <Label>
            <Checkbox {...checkbox("needsFundsForTravel")} />
            <FormattedMessage id="grants.form.fields.needsFundsForTravel.label" />
          </Label>
        </InputWrapper>

        <InputWrapper
          isRequired={true}
          errors={getErrors("occupation")}
          label={<FormattedMessage id="grants.form.fields.occupation" />}
        >
          <Select {...select("occupation")} required={true}>
            {OCCUPATION_OPTIONS.map(({ value, disabled, messageId }) => (
              <FormattedMessage id={messageId} key={messageId}>
                {(msg) => (
                  <option disabled={disabled} value={value}>
                    {msg}
                  </option>
                )}
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
            {INTERESTED_IN_VOLUNTEERING_OPTIONS.map(
              ({ value, disabled, messageId }) => (
                <FormattedMessage id={messageId} key={messageId}>
                  {(msg) => (
                    <option disabled={disabled} value={value}>
                      {msg}
                    </option>
                  )}
                </FormattedMessage>
              ),
            )}
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
            label={<FormattedMessage id="grants.form.fields.ageGroup" />}
            errors={getErrors("ageGroup")}
          >
            <Select {...select("ageGroup")} required={true}>
              {AGE_GROUPS_OPTIONS.map(({ value, disabled, messageId }) => (
                <FormattedMessage id={messageId} key={messageId}>
                  {(msg) => (
                    <option disabled={disabled} value={value}>
                      {msg}
                    </option>
                  )}
                </FormattedMessage>
              ))}
            </Select>
          </InputWrapper>

          <InputWrapper
            errors={getErrors("gender")}
            label={<FormattedMessage id="grants.form.fields.gender" />}
          >
            <Select>
              {GENDER_OPTIONS.map(({ value, disabled, messageId }) => (
                <FormattedMessage id={messageId} key={messageId}>
                  {(msg) => (
                    <option disabled={disabled} value={value}>
                      {msg}
                    </option>
                  )}
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
