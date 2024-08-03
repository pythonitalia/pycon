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
  Select,
  Spacer,
  Text,
  Textarea,
  VerticalStack,
} from "@python-italia/pycon-styleguide";
import type React from "react";
import { Fragment, useEffect } from "react";
import { FormattedMessage } from "react-intl";
import { useFormState } from "react-use-form-state";

import { useCurrentLanguage } from "~/locale/context";
import {
  type MultiLingualInput as MultiLingualInputType,
  type SendSubmissionMutation,
  type UpdateSubmissionMutation,
  useCfpFormQuery,
  useParticipantDataQuery,
} from "~/types";

import { useTranslatedMessage } from "~/helpers/use-translated-message";
import { createHref } from "../link";
import { MultiLingualInput } from "../multilingual-input";
import {
  type ParticipantFormFields,
  PublicProfileCard,
} from "../public-profile-card";
import { TagsSelect } from "../tags-select";

export type CfpFormFields = ParticipantFormFields & {
  type: string;
  title: { it?: string; en?: string };
  elevatorPitch: { it?: string; en?: string };
  length: string;
  audienceLevel: string;
  abstract: { it?: string; en?: string };
  notes: string;
  languages: string[];
  tags: string[];
  speakerLevel: string;
  previousTalkVideo: string;
  shortSocialSummary: string;
};

export type SubmissionStructure = {
  type: { id: string };
  title: string;
  elevatorPitch: string;
  abstract: string;
  multilingualTitle: { it: string; en: string };
  multilingualElevatorPitch: { it: string; en: string };
  multilingualAbstract: { it: string; en: string };
  duration: { id: string };
  audienceLevel: { id: string };
  languages: { code: string }[];
  notes: string;
  previousTalkVideo: string;
  speakerLevel: string;
  tags: { id: string }[];
  shortSocialSummary: string;
};

type Props = {
  onSubmit: (input: CfpFormFields) => void;
  submission?: SubmissionStructure | null;
  conferenceCode: string;
  loading: boolean;
  error: ApolloError | undefined;
  data: SendSubmissionMutation | UpdateSubmissionMutation;
};

const SPEAKER_LEVEL_OPTIONS = [
  {
    value: "",
    disabled: true,
    messageId: "cfp.selectSpeakerLevel",
  },
  {
    disabled: false,
    value: "new",
    messageId: "cfp.speakerLevel.new",
  },
  {
    disabled: false,
    value: "intermediate",
    messageId: "cfp.speakerLevel.intermediate",
  },
  {
    disabled: false,
    value: "experienced",
    messageId: "cfp.speakerLevel.experienced",
  },
];

const filterOutInactiveLanguages = (
  value: MultiLingualInputType,
  languages: string[],
): MultiLingualInputType => {
  return Object.entries(value).reduce((newDict, [key, value]) => {
    if (!languages.includes(key)) {
      return newDict;
    }

    newDict[key] = value;
    return newDict;
  }, {});
};

export const CfpForm = ({
  onSubmit,
  conferenceCode,
  submission,
  loading: submissionLoading,
  error: submissionError,
  data: submissionData,
}: Props) => {
  const language = useCurrentLanguage();
  const [formState, formOptions] = useFormState<CfpFormFields>(
    {
      title: {
        en: "",
        it: "",
      },
      abstract: {
        en: "",
        it: "",
      },
      elevatorPitch: {
        en: "",
        it: "",
      },
      languages: [],
    },
    {
      withIds: true,
    },
  );

  const { textarea, radio, select, checkbox, url, raw } = formOptions;

  const { data: conferenceData } = useCfpFormQuery({
    variables: {
      conference: conferenceCode,
    },
  });

  const { data: participantData } = useParticipantDataQuery({
    variables: {
      conference: conferenceCode,
    },
  });

  const submitSubmission = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    onSubmit({
      title: filterOutInactiveLanguages(
        formState.values.title,
        formState.values.languages,
      ),
      abstract: filterOutInactiveLanguages(
        formState.values.abstract,
        formState.values.languages,
      ),
      languages: formState.values.languages,
      type: formState.values.type,
      length: formState.values.length,
      elevatorPitch: filterOutInactiveLanguages(
        formState.values.elevatorPitch,
        formState.values.languages,
      ),
      notes: formState.values.notes,
      audienceLevel: formState.values.audienceLevel,
      tags: formState.values.tags,
      speakerLevel: formState.values.speakerLevel,
      previousTalkVideo: formState.values.previousTalkVideo,
      shortSocialSummary: formState.values.shortSocialSummary,
      participantWebsite: formState.values.participantWebsite,
      participantBio: formState.values.participantBio,
      participantTwitterHandle: formState.values.participantTwitterHandle,
      participantInstagramHandle: formState.values.participantInstagramHandle,
      participantLinkedinUrl: formState.values.participantLinkedinUrl,
      participantFacebookUrl: formState.values.participantFacebookUrl,
      participantMastodonHandle: formState.values.participantMastodonHandle,
      participantPhoto: formState.values.participantPhoto,
    });
  };

  const allowedDurations = conferenceData?.conference.durations.filter(
    (d) =>
      d.allowedSubmissionTypes.findIndex(
        (i) => i.id === formState.values.type,
      ) !== -1,
  );

  useEffect(() => {
    if (!allowedDurations?.length) {
      return;
    }

    // When changing format we need to reset to the first
    // available duration of the new format, but only if the
    // duration is not allowed

    if (
      !allowedDurations.find(
        (duration) => duration.id === formState.values.length,
      )
    ) {
      formState.setField("length", allowedDurations[0].id);
    }
  }, [formState.values.type]);

  useEffect(() => {
    if (submission) {
      formState.setField("type", submission!.type.id);
      formState.setField("title", submission!.multilingualTitle);
      formState.setField(
        "elevatorPitch",
        submission!.multilingualElevatorPitch,
      );
      formState.setField("length", submission!.duration.id);
      formState.setField("audienceLevel", submission!.audienceLevel.id);
      formState.setField(
        "languages",
        submission!.languages.map((l) => l.code),
      );
      formState.setField("abstract", submission!.multilingualAbstract);
      formState.setField("notes", submission!.notes);
      formState.setField(
        "tags",
        submission!.tags.map((t) => t.id),
      );
      formState.setField("shortSocialSummary", submission!.shortSocialSummary);
    }
  }, []);

  useEffect(() => {
    if (participantData.me.participant) {
      formState.setField("participantBio", participantData.me.participant.bio);
      formState.setField(
        "participantPhoto",
        participantData.me.participant.photoId,
      );
      formState.setField(
        "speakerLevel",
        participantData.me.participant.speakerLevel,
      );
      formState.setField(
        "previousTalkVideo",
        participantData.me.participant.previousTalkVideo,
      );
      formState.setField(
        "participantWebsite",
        participantData.me.participant.website,
      );
      formState.setField(
        "participantTwitterHandle",
        participantData.me.participant.twitterHandle,
      );
      formState.setField(
        "participantInstagramHandle",
        participantData.me.participant.instagramHandle,
      );
      formState.setField(
        "participantLinkedinUrl",
        participantData.me.participant.linkedinUrl,
      );
      formState.setField(
        "participantFacebookUrl",
        participantData.me.participant.facebookUrl,
      );
      formState.setField(
        "participantMastodonHandle",
        participantData.me.participant.mastodonHandle,
      );
    }
  }, []);

  const inputPlaceholder = useTranslatedMessage("input.placeholder");

  const hasValidationErrors =
    submissionData?.mutationOp.__typename === "SendSubmissionErrors";

  /* todo refactor to avoid multiple __typename? */
  const getErrors = (
    key:
      | "validationTitle"
      | "validationAbstract"
      | "validationLanguages"
      | "validationType"
      | "validationDuration"
      | "validationElevatorPitch"
      | "validationNotes"
      | "validationAudienceLevel"
      | "validationTags"
      | "validationSpeakerLevel"
      | "validationPreviousTalkVideo"
      | "validationShortSocialSummary"
      | "validationSpeakerBio"
      | "validationSpeakerWebsite"
      | "validationSpeakerPhoto"
      | "validationSpeakerTwitterHandle"
      | "validationSpeakerInstagramHandle"
      | "validationSpeakerLinkedinUrl"
      | "validationSpeakerFacebookUrl"
      | "validationSpeakerMastodonHandle"
      | "nonFieldErrors",
  ): string[] =>
    (submissionData?.mutationOp.__typename === "SendSubmissionErrors" &&
      submissionData!.mutationOp.errors[key]) ||
    [];

  return (
    <Fragment>
      <form onSubmit={submitSubmission} autoComplete="off">
        <MultiplePartsCard>
          <CardPart contentAlign="left">
            <Heading size={3}>
              <FormattedMessage id="cfp.youridea" />
            </Heading>
          </CardPart>
          <CardPart background="milk" contentAlign="left">
            <Grid cols={1} gap="medium">
              <InputWrapper
                required={true}
                title={<FormattedMessage id="cfp.choosetype" />}
                description={
                  <FormattedMessage id="cfp.choosetypeDescription" />
                }
              >
                <VerticalStack gap="small">
                  {conferenceData!.conference.submissionTypes.map((type) => (
                    <label key={type.id}>
                      <HorizontalStack gap="small" alignItems="center">
                        <Checkbox
                          {...radio("type", type.id)}
                          required={true}
                          size="small"
                        />
                        <Text weight="strong" size={2}>
                          {type.name}
                        </Text>
                      </HorizontalStack>
                    </label>
                  ))}
                </VerticalStack>
              </InputWrapper>

              <InputWrapper
                required={true}
                title={<FormattedMessage id="cfp.languagesLabel" />}
                description={<FormattedMessage id="cfp.languagesDescription" />}
              >
                <HorizontalStack gap="small">
                  {conferenceData!.conference.languages.map((language) => (
                    <label key={language.code}>
                      <HorizontalStack gap="small" alignItems="center">
                        <Checkbox
                          size="small"
                          {...checkbox("languages", language.code)}
                        />
                        <Text weight="strong" size={2}>
                          {language.name}
                        </Text>
                      </HorizontalStack>
                    </label>
                  ))}
                </HorizontalStack>
              </InputWrapper>

              <InputWrapper
                required={true}
                title={<FormattedMessage id="cfp.title" />}
                description={<FormattedMessage id="cfp.titleDescription" />}
              >
                <MultiLingualInput
                  {...raw("title")}
                  languages={formState.values.languages}
                >
                  <Input
                    required={true}
                    maxLength={100}
                    errors={getErrors("validationTitle")}
                    placeholder={inputPlaceholder}
                  />
                </MultiLingualInput>
              </InputWrapper>

              <InputWrapper
                required={true}
                title={<FormattedMessage id="cfp.elevatorPitchLabel" />}
                description={
                  <FormattedMessage id="cfp.elevatorPitchDescription" />
                }
              >
                <MultiLingualInput
                  {...raw("elevatorPitch")}
                  languages={formState.values.languages}
                >
                  <Textarea
                    required={true}
                    maxLength={300}
                    rows={6}
                    errors={getErrors("validationElevatorPitch")}
                    placeholder={inputPlaceholder}
                  />
                </MultiLingualInput>
              </InputWrapper>

              <InputWrapper
                required={true}
                title={<FormattedMessage id="cfp.lengthLabel" />}
                description={<FormattedMessage id="cfp.lengthDescription" />}
              >
                <Select
                  {...select("length")}
                  required={true}
                  errors={getErrors("validationDuration")}
                >
                  <FormattedMessage id="cfp.selectDuration">
                    {(txt) => (
                      <option value="" disabled={true}>
                        {txt}
                      </option>
                    )}
                  </FormattedMessage>
                  {allowedDurations!.map((d) => (
                    <option key={d.id} value={d.id}>
                      {d.name}
                    </option>
                  ))}
                </Select>
              </InputWrapper>

              <InputWrapper
                required={true}
                title={<FormattedMessage id="cfp.audienceLevelLabel" />}
                description={
                  <FormattedMessage id="cfp.audienceLevelDescription" />
                }
              >
                <Select
                  {...select("audienceLevel")}
                  required={true}
                  errors={getErrors("validationAudienceLevel")}
                >
                  <FormattedMessage id="cfp.selectAudience">
                    {(txt) => (
                      <option value="" disabled={true}>
                        {txt}
                      </option>
                    )}
                  </FormattedMessage>
                  {conferenceData!.conference.audienceLevels.map((a) => (
                    <option key={a.id} value={a.id}>
                      {a.name}
                    </option>
                  ))}
                </Select>
              </InputWrapper>

              <InputWrapper
                required={true}
                title={<FormattedMessage id="cfp.tagsLabel" />}
                description={<FormattedMessage id="cfp.tagsDescription" />}
              >
                <TagsSelect
                  tags={formState.values.tags || []}
                  onChange={(tags: { value: string }[]) => {
                    formState.setField(
                      "tags",
                      tags.map((t) => t.value),
                    );
                  }}
                />
              </InputWrapper>

              <InputWrapper
                required={true}
                title={<FormattedMessage id="cfp.abstractLabel" />}
                description={<FormattedMessage id="cfp.abstractDescription" />}
              >
                <MultiLingualInput
                  {...raw("abstract")}
                  languages={formState.values.languages}
                >
                  <Textarea
                    required={true}
                    maxLength={5000}
                    rows={6}
                    errors={getErrors("validationAbstract")}
                    placeholder={inputPlaceholder}
                  />
                </MultiLingualInput>
              </InputWrapper>

              <InputWrapper
                title={<FormattedMessage id="cfp.notesLabel" />}
                description={<FormattedMessage id="cfp.notesDescription" />}
              >
                <Textarea
                  {...textarea("notes")}
                  maxLength={1000}
                  rows={4}
                  errors={getErrors("validationNotes")}
                  placeholder={inputPlaceholder}
                />
              </InputWrapper>

              <InputWrapper
                required={false}
                title={<FormattedMessage id="cfp.shortSocialSummaryLabel" />}
                description={
                  <FormattedMessage id="cfp.shortSocialSummaryDescription" />
                }
              >
                <Textarea
                  {...textarea("shortSocialSummary")}
                  required={false}
                  maxLength={128}
                  rows={2}
                  errors={getErrors("validationShortSocialSummary")}
                  placeholder={inputPlaceholder}
                />
              </InputWrapper>
            </Grid>
          </CardPart>
        </MultiplePartsCard>

        <Spacer size="medium" />

        <MultiplePartsCard>
          <CardPart contentAlign="left">
            <Heading size={3}>
              <FormattedMessage id="cfp.aboutYou" />
            </Heading>
          </CardPart>
          <CardPart background="milk" contentAlign="left">
            <Grid cols={1} gap="medium">
              <Text size={2}>
                <FormattedMessage id="cfp.aboutYouDescription" />
              </Text>
              <InputWrapper
                required={true}
                title={<FormattedMessage id="cfp.speakerLevel" />}
                description={
                  <FormattedMessage id="cfp.speakerLevelDescription" />
                }
              >
                <Select
                  {...select("speakerLevel")}
                  required={true}
                  errors={getErrors("validationSpeakerLevel")}
                >
                  {SPEAKER_LEVEL_OPTIONS.map(
                    ({ value, disabled, messageId }) => (
                      <FormattedMessage id={messageId} key={messageId}>
                        {(copy) => (
                          <option disabled={disabled} value={value}>
                            {copy}
                          </option>
                        )}
                      </FormattedMessage>
                    ),
                  )}
                </Select>
              </InputWrapper>

              <InputWrapper
                title={<FormattedMessage id="cfp.previousTalkVideo" />}
                description={
                  <FormattedMessage id="cfp.previousTalkVideoDescription" />
                }
              >
                <Input
                  {...url("previousTalkVideo")}
                  required={false}
                  maxLength={2048}
                  errors={getErrors("validationPreviousTalkVideo")}
                />
              </InputWrapper>
            </Grid>
          </CardPart>
        </MultiplePartsCard>

        <Spacer size="medium" />

        <PublicProfileCard
          me={participantData.me}
          formOptions={formOptions}
          getParticipantValidationError={(field) =>
            getErrors(
              `validationSpeaker${field[0].toUpperCase()}${field.substring(1)}` as any,
            )
          }
        />

        <Spacer size="medium" />

        <Grid cols={2}>
          <div>
            <Text weight="strong" uppercase color="grey-900" size="label3">
              <FormattedMessage id="cfp.grantsLabel" />
            </Text>
            <Spacer size="thin" />
            <Text color="grey-700" size="label3">
              <FormattedMessage
                id="cfp.grantsCheckbox"
                values={{
                  grantsCta: (
                    <Link
                      href={createHref({
                        path: "/grants-info",
                        locale: language,
                      })}
                      target="_blank"
                    >
                      <Text
                        decoration="underline"
                        color="grey-700"
                        hoverColor="green"
                        size="label3"
                      >
                        <FormattedMessage id="cfp.grantsCta" />
                      </Text>
                    </Link>
                  ),
                }}
              />
            </Text>
          </div>
          <div className="flex justify-center items-end flex-col">
            {(hasValidationErrors || submissionError?.message) && (
              <Text size="label3" color="red">
                <FormattedMessage id="cfp.validationErrors" />
              </Text>
            )}
            <Spacer size="small" />
            <Button
              variant="secondary"
              disabled={
                submissionLoading ||
                submissionData?.mutationOp?.__typename === "Submission"
              }
            >
              {submissionLoading && <FormattedMessage id="cfp.loading" />}
              {!submissionLoading && <FormattedMessage id="cfp.submit" />}
            </Button>
          </div>
        </Grid>
      </form>
    </Fragment>
  );
};
