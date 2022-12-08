/** @jsxRuntime classic */

/** @jsx jsx */
import { ApolloError } from "@apollo/client";
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

import { Alert } from "~/components/alert";
import { Button } from "~/components/button/button";
import { InputWrapper } from "~/components/input-wrapper";
import { Link } from "~/components/link";
import { MyGrant } from "~/components/profile/my-grant";
import { useCurrentUser } from "~/helpers/use-current-user";
import {
  Grant,
  UpdateGrantInput,
  useSendGrantMutation,
  useMyGrantQuery,
  SendGrantInput,
  SendGrantMutation,
  UpdateGrantMutation,
} from "~/types";

import { ErrorsList } from "../errors-list";
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

export const MyGrantOrForm = () => {
  const code = process.env.conferenceCode;

  const { error, data } = useMyGrantQuery({
    errorPolicy: "all",
    variables: {
      conference: code,
    },
    skip: typeof window === "undefined",
  });
  const grant = data && data?.me?.grant;

  const [submitGrant, { loading, error: grantError }] = useSendGrantMutation();

  const onSubmit = async (input: SendGrantInput) => {
    submitGrant({
      variables: {
        input,
      },
    });
  };

  if (error) {
    return <Alert variant="alert">{error.message}</Alert>;
  }

  if (grant) {
    return <MyGrant />;
  }

  return (
    <>
      <Heading mb={4} as="h1">
        <FormattedMessage id="grants.form.title" />
      </Heading>
      <GrantForm
        conference={code}
        onSubmit={onSubmit}
        error={grantError}
        data={data}
        loading={loading}
      />
    </>
  );
};

type GrantFormProps = {
  conference: string;
  grant?: Grant | null;
  onSubmit: (input: SendGrantInput | UpdateGrantInput) => void;
  loading: boolean;
  error: ApolloError | null;
  data: SendGrantMutation | UpdateGrantMutation;
};

export const GrantForm = ({
  conference,
  grant,
  onSubmit,
  loading: grantLoading,
  error: grantError,
  data: grantData,
}: GrantFormProps) => {
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
    // to not override if we are editing the grant
    if (user && !grant) {
      formState.setField("fullName", user.fullName);
      formState.setField("name", user.name);
      formState.setField("gender", user.gender);
      if (user.dateBirth) {
        const age =
          new Date().getFullYear() - new Date(user.dateBirth).getFullYear();
        formState.setField(
          "ageGroup",
          AGE_GROUPS_OPTIONS.find(
            (option) => option.isAgeInRange && option.isAgeInRange(age),
          ).value,
        );
      }
    }
  }, [user]);

  useEffect(() => {
    if (grant) {
      console.log(grant);
      formState.setField("fullName", grant.fullName);
      formState.setField("name", grant.name);
      formState.setField("gender", grant.gender);
      formState.setField("grantType", grant.grantType);
      formState.setField("occupation", grant.occupation);
      formState.setField("ageGroup", grant.ageGroup.toLowerCase());
      formState.setField("pythonUsage", grant.pythonUsage);
      formState.setField("beenToOtherEvents", grant.beenToOtherEvents);
      formState.setField(
        "interestedInVolunteering",
        grant.interestedInVolunteering,
      );
      formState.setField("needsFundsForTravel", grant.needsFundsForTravel);
      formState.setField("why", grant.why);
      formState.setField("notes", grant.notes);
      formState.setField("travellingFrom", grant.travellingFrom);
    }
  }, [grant]);

  const handleOnSubmit = useCallback(
    async (e: React.FormEvent<HTMLFormElement>) => {
      e.preventDefault();
      onSubmit({
        conference,
        ageGroup: formState.values.ageGroup.toLowerCase(),
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
      });
    },
    [formState.values],
  );

  const getErrors = (
    key: keyof GrantFormFields | "nonFieldErrors",
  ): string[] => {
    if (grantData?.mutationOp.__typename === "GrantErrors") {
      let errorKey: string = key;

      if (key !== "nonFieldErrors") {
        const capitalized = key.charAt(0).toUpperCase() + key.slice(1);
        errorKey = `validation${capitalized}`;
      }

      return (grantData.mutationOp as any)[errorKey];
    }

    return [];
  };

  if (!grantLoading && grantData?.mutationOp.__typename === "Grant") {
    return (
      <Text>
        <FormattedMessage
          id="grants.form.sent"
          values={{
            linkGrant: (
              <Link
                path={`/grants/edit`}
                sx={{
                  textDecoration: "underline",
                }}
              >
                <FormattedMessage id="grants.form.sent.linkGrant.text" />
              </Link>
            ),
          }}
        />
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
      <form onSubmit={handleOnSubmit}>
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

        <InputWrapper
          isRequired={true}
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

        <Box>
          <Heading sx={{ mb: 2 }}>
            <FormattedMessage id="grants.form.optionalInformation" />
          </Heading>

          <Text sx={{ mb: 3 }}>
            <FormattedMessage id="grants.form.optionalInformation.description" />
          </Text>

          <InputWrapper
            errors={getErrors("gender")}
            label={<FormattedMessage id="grants.form.fields.gender" />}
          >
            <Select {...select("gender")}>
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

        {grantError && (
          <Alert sx={{ mb: 4 }} variant="alert">
            <FormattedMessage
              id="global.tryAgain"
              values={{ error: grantError.message }}
            />
          </Alert>
        )}

        {grantLoading && (
          <Alert
            sx={{
              mb: 3,
            }}
            variant="info"
          >
            <FormattedMessage id="grants.form.sendingRequest" />
          </Alert>
        )}

        <Button loading={grantLoading}>
          <FormattedMessage id="grants.form.submit" />
        </Button>
      </form>
    </Fragment>
  );
};
