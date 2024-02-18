/** @jsxRuntime classic */

/** @jsx jsx */
import { ApolloError } from "@apollo/client";
import {
  Button,
  CardPart,
  Checkbox,
  Grid,
  Heading,
  HorizontalStack,
  Input,
  InputWrapper,
  Link,
  MultiplePartsCard,
  Section,
  Select,
  Spacer,
  Text,
  Textarea,
} from "@python-italia/pycon-styleguide";
import React, { useCallback, useEffect } from "react";
import { FormattedMessage } from "react-intl";
import { useFormState } from "react-use-form-state";
import { jsx } from "theme-ui";

import { Alert } from "~/components/alert";
import { MyGrant } from "~/components/profile/my-grant";
import { useCountries } from "~/helpers/use-countries";
import { useCurrentUser } from "~/helpers/use-current-user";
import { useTranslatedMessage } from "~/helpers/use-translated-message";
import { useCurrentLanguage } from "~/locale/context";
import {
  AgeGroup,
  Grant,
  GrantType,
  InterestedInVolunteering,
  Occupation,
  SendGrantInput,
  SendGrantMutation,
  UpdateGrantInput,
  UpdateGrantMutation,
  useMyGrantQuery,
  useSendGrantMutation,
} from "~/types";

import { ErrorsList } from "../errors-list";
import { createHref } from "../link";
import {
  AGE_GROUPS_OPTIONS,
  GENDER_OPTIONS,
  GRANT_TYPE_OPTIONS,
  INTERESTED_IN_VOLUNTEERING_OPTIONS,
  OCCUPATION_OPTIONS,
} from "./options";

export type GrantFormFields = {
  name: string;
  fullName: string;
  ageGroup: AgeGroup;
  gender: string;
  occupation: Occupation;
  grantType: GrantType;
  pythonUsage: string;
  communityContribution: string;
  beenToOtherEvents: string;
  interestedInVolunteering: InterestedInVolunteering;
  needsFundsForTravel: string;
  needVisa: string;
  needAccommodation: string;
  why: string;
  notes: string;
  travellingFrom: string;
  website: string;
  twitterHandle: string;
  githubHandle: string;
  linkedinUrl: string;
  mastodonHandle: string;
  acceptedPrivacyPolicy: boolean;
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
  const grant = data?.me?.grant;

  const [submitGrant, { loading, error: grantError, data: grantData }] =
    useSendGrantMutation({
      onError(err) {
        console.log(err.message);
      },
    });

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
      <Section>
        <Heading size="display2">
          <FormattedMessage id="grants.form.title" />
        </Heading>
        <Spacer size="medium" />
        <Text size={2}>
          <FormattedMessage id="grants.form.description" />
        </Text>
      </Section>
      <Section>
        <GrantForm
          conference={code}
          onSubmit={onSubmit}
          error={grantError}
          data={grantData}
          loading={loading}
        />
      </Section>
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
  const language = useCurrentLanguage();
  const countries = useCountries();

  const inputPlaceholderText = useTranslatedMessage("input.placeholder");
  const { user, loading: loadingUser } = useCurrentUser({});
  const [formState, { text, textarea, select, checkbox }] =
    useFormState<GrantFormFields>(
      {
        needsFundsForTravel: "false",
      },
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
          AGE_GROUPS_OPTIONS.find((option) => option.isAgeInRange?.(age)).value,
        );
      }
    }
  }, [user]);

  useEffect(() => {
    if (grant) {
      formState.setField("fullName", grant.fullName);
      formState.setField("name", grant.name);
      formState.setField("gender", grant.gender);
      formState.setField("grantType", grant.grantType);
      formState.setField("occupation", grant.occupation);
      formState.setField("ageGroup", grant.ageGroup);
      formState.setField("pythonUsage", grant.pythonUsage);
      formState.setField("communityContribution", grant.communityContribution);
      formState.setField("beenToOtherEvents", grant.beenToOtherEvents);
      formState.setField(
        "interestedInVolunteering",
        grant.interestedInVolunteering,
      );
      formState.setField(
        "needsFundsForTravel",
        grant.needsFundsForTravel.toString(),
      );
      formState.setField("needVisa", grant.needVisa.toString());
      formState.setField(
        "needAccommodation",
        grant.needAccommodation.toString(),
      );
      formState.setField("why", grant.why);
      formState.setField("notes", grant.notes);
      formState.setField("travellingFrom", grant.travellingFrom);
      formState.setField("website", grant.website);
      formState.setField("twitterHandle", grant.twitterHandle);
      formState.setField("githubHandle", grant.githubHandle);
      formState.setField("linkedinUrl", grant.linkedinUrl);
      formState.setField("mastodonHandle", grant.mastodonHandle);
      formState.setField("acceptedPrivacyPolicy", true);
    }
  }, [grant]);

  const handleOnSubmit = useCallback(
    async (e: React.FormEvent<HTMLFormElement>) => {
      e.preventDefault();
      onSubmit({
        conference,
        ageGroup: formState.values.ageGroup,
        fullName: formState.values.fullName,
        name: formState.values.name,
        gender: formState.values.gender,
        beenToOtherEvents: formState.values.beenToOtherEvents,
        interestedInVolunteering: formState.values.interestedInVolunteering,
        notes: formState.values.notes,
        grantType: formState.values.grantType,
        needsFundsForTravel: formState.values.needsFundsForTravel === "true",
        why: formState.values.why,
        travellingFrom: formState.values.travellingFrom,
        occupation: formState.values.occupation,
        pythonUsage: formState.values.pythonUsage,
        communityContribution: formState.values.communityContribution,
        needVisa: formState.values.needVisa === "true",
        needAccommodation: formState.values.needAccommodation === "true",
        website: formState.values.website,
        twitterHandle: formState.values.twitterHandle,
        githubHandle: formState.values.githubHandle,
        linkedinUrl: formState.values.linkedinUrl,
        mastodonHandle: formState.values.mastodonHandle,
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

      return (grantData.mutationOp as any).errors[errorKey];
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
                href={createHref({ path: "/grants/edit", locale: language })}
              >
                <Text
                  color="none"
                  decoration="underline"
                  size="inherit"
                  weight="strong"
                >
                  <FormattedMessage id="grants.form.sent.linkGrant.text" />
                </Text>
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

  const hasValidationErrors =
    grantData?.mutationOp.__typename === "GrantErrors";
  const nonFieldErrors = getErrors("nonFieldErrors");

  return (
    <form onSubmit={handleOnSubmit}>
      <MultiplePartsCard>
        <CardPart contentAlign="left">
          <Heading size={3}>
            <FormattedMessage id="grants.form.aboutYou" />
          </Heading>
        </CardPart>
        <CardPart background="milk" contentAlign="left">
          <Grid cols={1}>
            <InputWrapper
              required={true}
              title={<FormattedMessage id="grants.form.fields.fullName" />}
              description={
                <FormattedMessage id="grants.form.fields.fullName.description" />
              }
            >
              <Input
                errors={getErrors("fullName")}
                {...text("fullName")}
                required={true}
                placeholder={inputPlaceholderText}
              />
            </InputWrapper>

            <InputWrapper
              required={false}
              title={<FormattedMessage id="grants.form.fields.name" />}
              description={
                <FormattedMessage id="grants.form.fields.name.description" />
              }
            >
              <Input
                {...text("name")}
                errors={getErrors("name")}
                placeholder={inputPlaceholderText}
                required={false}
              />
            </InputWrapper>
            <InputWrapper
              required={true}
              title={<FormattedMessage id="grants.form.fields.ageGroup" />}
              description={
                <FormattedMessage id="grants.form.fields.ageGroup.description" />
              }
            >
              <Select
                {...select("ageGroup")}
                required={true}
                errors={getErrors("ageGroup")}
              >
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
              required={true}
              title={<FormattedMessage id="grants.form.fields.occupation" />}
              description={
                <FormattedMessage id="grants.form.fields.occupation.description" />
              }
            >
              <Select
                {...select("occupation")}
                required={true}
                errors={getErrors("occupation")}
              >
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
          </Grid>
        </CardPart>
      </MultiplePartsCard>
      <Spacer size="medium" />

      <MultiplePartsCard>
        <CardPart contentAlign="left">
          <Heading size={3}>
            <FormattedMessage id="grants.form.yourGrant" />
          </Heading>
        </CardPart>
        <CardPart contentAlign="left" background="milk">
          <Grid cols={1}>
            <InputWrapper
              required={true}
              title={<FormattedMessage id="grants.form.fields.grantType" />}
              description={
                <FormattedMessage id="grants.form.fields.grantType.description" />
              }
            >
              <Select
                {...select("grantType")}
                required={true}
                errors={getErrors("grantType")}
              >
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
              required={true}
              title={
                <FormattedMessage id="grants.form.fields.travellingFrom" />
              }
              description={
                <FormattedMessage id="grants.form.fields.travellingFrom.description" />
              }
            >
              <Select
                {...select("travellingFrom")}
                required={true}
                errors={getErrors("travellingFrom")}
              >
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

            <InputWrapper
              title={
                <FormattedMessage id="grants.form.fields.needsFundsForTravel" />
              }
              description={
                <FormattedMessage id="grants.form.fields.needsFundsForTravel.description" />
              }
            >
              <Select {...select("needsFundsForTravel")}>
                <FormattedMessage id="global.no">
                  {(msg) => <option value="false">{msg}</option>}
                </FormattedMessage>
                <FormattedMessage id="global.yes">
                  {(msg) => <option value="true">{msg}</option>}
                </FormattedMessage>
              </Select>
            </InputWrapper>

            <InputWrapper
              title={<FormattedMessage id="grants.form.fields.needVisa" />}
              description={
                <FormattedMessage id="grants.form.fields.needVisa.description" />
              }
            >
              <Select {...select("needVisa")}>
                <FormattedMessage id="global.no">
                  {(msg) => <option value="false">{msg}</option>}
                </FormattedMessage>
                <FormattedMessage id="global.yes">
                  {(msg) => <option value="true">{msg}</option>}
                </FormattedMessage>
              </Select>
            </InputWrapper>

            <InputWrapper
              title={
                <FormattedMessage id="grants.form.fields.needAccommodation" />
              }
              description={
                <FormattedMessage id="grants.form.fields.needAccommodation.description" />
              }
            >
              <Select {...select("needAccommodation")}>
                <FormattedMessage id="global.no">
                  {(msg) => <option value="false">{msg}</option>}
                </FormattedMessage>
                <FormattedMessage id="global.yes">
                  {(msg) => <option value="true">{msg}</option>}
                </FormattedMessage>
              </Select>
            </InputWrapper>

            <InputWrapper
              required={true}
              title={<FormattedMessage id="grants.form.fields.why" />}
              description={
                <FormattedMessage id="grants.form.fields.why.description" />
              }
            >
              <Textarea
                {...textarea("why")}
                rows={2}
                required={true}
                placeholder={inputPlaceholderText}
                errors={getErrors("why")}
              />
            </InputWrapper>

            <InputWrapper
              required={true}
              title={
                <FormattedMessage id="grants.form.fields.interestedInVolunteering" />
              }
              description={
                <FormattedMessage id="grants.form.fields.interestedInVolunteering.description" />
              }
            >
              <Select
                {...select("interestedInVolunteering")}
                required={true}
                errors={getErrors("interestedInVolunteering")}
              >
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
          </Grid>
        </CardPart>
      </MultiplePartsCard>
      <Spacer size="medium" />

      <MultiplePartsCard>
        <CardPart contentAlign="left">
          <Heading size={3}>
            <FormattedMessage id="grants.form.youAndPython" />
          </Heading>
        </CardPart>
        <CardPart contentAlign="left" background="milk">
          <Grid cols={1}>
            <InputWrapper
              required={true}
              title={<FormattedMessage id="grants.form.fields.pythonUsage" />}
              description={
                <FormattedMessage id="grants.form.fields.pythonUsage.description" />
              }
            >
              <Textarea
                {...textarea("pythonUsage")}
                rows={2}
                required={true}
                placeholder={inputPlaceholderText}
                errors={getErrors("pythonUsage")}
              />
            </InputWrapper>

            <InputWrapper
              required={true}
              title={
                <FormattedMessage id="grants.form.fields.beenToOtherEvents" />
              }
              description={
                <FormattedMessage id="grants.form.fields.beenToOtherEvents.description" />
              }
            >
              <Textarea
                {...textarea("beenToOtherEvents")}
                rows={2}
                required={true}
                errors={getErrors("beenToOtherEvents")}
                placeholder={inputPlaceholderText}
              />
            </InputWrapper>

            <InputWrapper
              required={false}
              title={
                <FormattedMessage id="grants.form.fields.communityContribution" />
              }
              description={
                <FormattedMessage id="grants.form.fields.communityContribution.description" />
              }
            >
              <Textarea
                {...textarea("communityContribution")}
                rows={2}
                required={false}
                errors={getErrors("communityContribution")}
                placeholder={inputPlaceholderText}
              />
            </InputWrapper>
          </Grid>
        </CardPart>
      </MultiplePartsCard>

      <Spacer size="medium" />

      <MultiplePartsCard>
        <CardPart contentAlign="left">
          <Heading size={3}>
            <FormattedMessage id="grants.form.optionalInformation" />
          </Heading>
        </CardPart>
        <CardPart background="milk" contentAlign="left">
          <Grid cols={1}>
            <InputWrapper
              title={<FormattedMessage id="grants.form.fields.gender" />}
              description={
                <FormattedMessage id="grants.form.fields.gender.description" />
              }
            >
              <Select {...select("gender")} errors={getErrors("gender")}>
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
              title={<FormattedMessage id="grants.form.fields.notes" />}
              description={
                <FormattedMessage id="grants.form.fields.notes.description" />
              }
            >
              <Textarea
                {...textarea("notes")}
                errors={getErrors("notes")}
                placeholder={inputPlaceholderText}
              />
            </InputWrapper>

            <InputWrapper
              title={<FormattedMessage id="grants.form.fields.website" />}
            >
              <Input
                {...text("website")}
                errors={getErrors("website")}
                placeholder={inputPlaceholderText}
              />
            </InputWrapper>

            <InputWrapper
              title={<FormattedMessage id="grants.form.fields.linkedinUrl" />}
            >
              <Input
                {...text("linkedinUrl")}
                errors={getErrors("linkedinUrl")}
                placeholder={inputPlaceholderText}
              />
            </InputWrapper>

            <InputWrapper
              title={<FormattedMessage id="grants.form.fields.githubHandle" />}
            >
              <Input
                {...text("githubHandle")}
                errors={getErrors("githubHandle")}
                placeholder={inputPlaceholderText}
              />
            </InputWrapper>

            <InputWrapper
              title={<FormattedMessage id="grants.form.fields.twitterHandle" />}
            >
              <Input
                {...text("twitterHandle")}
                errors={getErrors("twitterHandle")}
                placeholder={inputPlaceholderText}
              />
            </InputWrapper>
            <InputWrapper
              title={
                <FormattedMessage id="grants.form.fields.mastodonHandle" />
              }
            >
              <Input
                {...text("mastodonHandle")}
                errors={getErrors("mastodonHandle")}
                placeholder={inputPlaceholderText}
              />
            </InputWrapper>
          </Grid>
        </CardPart>
      </MultiplePartsCard>

      {!grant && (
        <>
          <Spacer size="small" />
          <Text size={2}>
            <FormattedMessage
              id="grants.form.privacyPolicyHeading"
              values={{
                link: (
                  <Link
                    className="underline"
                    target="_blank"
                    href={createHref({
                      path: "/privacy-policy",
                      locale: language,
                    })}
                  >
                    Privacy Policy
                  </Link>
                ),
              }}
            />
          </Text>
          <Spacer size="small" />

          <label>
            <HorizontalStack gap="small" alignItems="center">
              <Checkbox
                {...checkbox("acceptedPrivacyPolicy")}
                checked={formState.values.acceptedPrivacyPolicy}
              />
              <Text size={2} weight="strong">
                <FormattedMessage
                  id="grants.form.acceptPrivacyPolicy"
                  values={{
                    link: (
                      <Link
                        className="underline"
                        target="_blank"
                        href={createHref({
                          path: "/privacy-policy",
                          locale: language,
                        })}
                      >
                        Privacy Policy
                      </Link>
                    ),
                  }}
                />
              </Text>
            </HorizontalStack>
          </label>
        </>
      )}

      <Spacer size="large" />

      <HorizontalStack
        wrap="wrap"
        alignItems="center"
        gap="medium"
        justifyContent="spaceBetween"
      >
        <div>
          <ErrorsList
            sx={{ mb: 3 }}
            errors={[
              ...nonFieldErrors,
              ...(grantError ? [grantError.message] : []),
              ...(nonFieldErrors.length === 0 && hasValidationErrors
                ? [<FormattedMessage id="grants.form.validationErrors" />]
                : []),
            ]}
          />
        </div>
        <Button
          disabled={grantLoading || !formState.values.acceptedPrivacyPolicy}
        >
          <FormattedMessage id="grants.form.submit" />
        </Button>
      </HorizontalStack>
    </form>
  );
};
