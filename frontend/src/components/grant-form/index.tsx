import type { ApolloError } from "@apollo/client";
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
import type React from "react";
import { useCallback, useEffect } from "react";
import { FormattedMessage } from "react-intl";
import { useFormState } from "react-use-form-state";

import { Alert } from "~/components/alert";
import { useCountries } from "~/helpers/use-countries";
import { useCurrentUser } from "~/helpers/use-current-user";
import { useTranslatedMessage } from "~/helpers/use-translated-message";
import { useCurrentLanguage } from "~/locale/context";
import {
  type AgeGroup,
  type Grant,
  type GrantType,
  type Occupation,
  type SendGrantInput,
  type SendGrantMutation,
  type UpdateGrantInput,
  type UpdateGrantMutation,
  useGrantDeadlineQuery,
  useParticipantDataQuery,
  useSendGrantMutation,
} from "~/types";
import { ErrorsList } from "../errors-list";
import { createHref } from "../link";
import {
  type ParticipantFormFields,
  PublicProfileCard,
} from "../public-profile-card";
import {
  AGE_GROUPS_OPTIONS,
  GENDER_OPTIONS,
  GRANT_TYPE_OPTIONS,
  OCCUPATION_OPTIONS,
} from "./options";

export type GrantFormFields = ParticipantFormFields & {
  name: string;
  fullName: string;
  ageGroup: AgeGroup;
  gender: string;
  occupation: Occupation;
  grantType: GrantType;
  pythonUsage: string;
  communityContribution: string;
  beenToOtherEvents: string;
  needsFundsForTravel: string;
  needVisa: string;
  needAccommodation: string;
  why: string;
  notes: string;
  travellingFrom: string;
  acceptedPrivacyPolicy: boolean;
};

export const GrantSendForm = () => {
  const code = process.env.conferenceCode;

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

  const {
    data: {
      conference: { deadline },
    },
  } = useGrantDeadlineQuery({
    variables: {
      conference: conference,
    },
  });

  const inputPlaceholderText = useTranslatedMessage("input.placeholder");
  const { user, loading: loadingUser } = useCurrentUser({});
  const [formState, formOptions] = useFormState<GrantFormFields>(
    {},
    {
      withIds: true,
    },
  );
  const { textarea, select, checkbox, text } = formOptions;

  const dateFormatter = new Intl.DateTimeFormat(language, {
    day: "numeric",
    month: "long",
    year: "numeric",
  });

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

      if (grant.participant) {
        formState.setField("participantBio", grant.participant.bio);
        formState.setField("participantWebsite", grant.participant.website);
        formState.setField(
          "participantTwitterHandle",
          grant.participant.twitterHandle,
        );
        formState.setField(
          "participantInstagramHandle",
          grant.participant.instagramHandle,
        );
        formState.setField(
          "participantLinkedinUrl",
          grant.participant.linkedinUrl,
        );
        formState.setField(
          "participantFacebookUrl",
          grant.participant.facebookUrl,
        );
        formState.setField(
          "participantMastodonHandle",
          grant.participant.mastodonHandle,
        );
      }
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
        participantWebsite: formState.values.participantWebsite,
        participantBio: formState.values.participantBio,
        participantTwitterHandle: formState.values.participantTwitterHandle,
        participantInstagramHandle: formState.values.participantInstagramHandle,
        participantLinkedinUrl: formState.values.participantLinkedinUrl,
        participantFacebookUrl: formState.values.participantFacebookUrl,
        participantMastodonHandle: formState.values.participantMastodonHandle,
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
            linkMyGrant: (
              <Link
                href={createHref({
                  path: "/profile/my-grant",
                  locale: language,
                })}
              >
                <Text
                  color="none"
                  decoration="underline"
                  size="inherit"
                  weight="strong"
                >
                  <FormattedMessage id="grants.form.sent.linkMyGrant.text" />
                </Text>
              </Link>
            ),
            grantsDeadline: dateFormatter.format(new Date(deadline.end)),
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
    <form onSubmit={handleOnSubmit} autoComplete="off">
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
              required={true}
            >
              <Select {...select("needsFundsForTravel")} required={true}>
                <FormattedMessage id="global.selectOption">
                  {(msg) => <option value="">{msg}</option>}
                </FormattedMessage>
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
              required={true}
            >
              <Select {...select("needVisa")} required={true}>
                <FormattedMessage id="global.selectOption">
                  {(msg) => <option value="">{msg}</option>}
                </FormattedMessage>
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
              required={true}
            >
              <Select {...select("needAccommodation")} required={true}>
                <FormattedMessage id="global.selectOption">
                  {(msg) => <option value="">{msg}</option>}
                </FormattedMessage>
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
          </Grid>
        </CardPart>
      </MultiplePartsCard>

      <Spacer size="medium" />

      <PublicProfileCard
        formOptions={formOptions}
        photoRequired={false}
        getParticipantValidationError={(field) =>
          getErrors(
            `validationSpeaker${field[0].toUpperCase()}${field.substring(1)}` as any,
          )
        }
        showPhotoField={false}
      />

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
                  id="global.acceptPrivacyPolicy"
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
            className="mb-1"
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
          variant="secondary"
        >
          <FormattedMessage id="grants.form.submit" />
        </Button>
      </HorizontalStack>
    </form>
  );
};
