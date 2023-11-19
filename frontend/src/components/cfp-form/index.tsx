/** @jsxRuntime classic */

/** @jsx jsx */
import { ApolloError } from "@apollo/client";
import { Button, Link } from "@python-italia/pycon-styleguide";
import React, { Fragment, useEffect } from "react";
import { FormattedMessage } from "react-intl";
import { useFormState } from "react-use-form-state";
import {
  Box,
  Checkbox,
  Flex,
  Grid,
  jsx,
  Label,
  Radio,
  Select,
  Text,
  Heading,
} from "theme-ui";

import { useCurrentLanguage } from "~/locale/context";
import {
  MultiLingualInput as MultiLingualInputType,
  SendSubmissionMutation,
  UpdateSubmissionMutation,
  useCfpFormQuery,
  useParticipantDataQuery,
} from "~/types";

import { Alert } from "../alert";
import { FileInput } from "../file-input";
import { TagLine } from "../input-tag";
import { InputWrapper } from "../input-wrapper";
import { Input, Textarea } from "../inputs";
import { createHref } from "../link";
import { MultiLingualInput } from "../multilingual-input";

export type CfpFormFields = {
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
  speakerBio: string;
  speakerPhoto: any;
  speakerWebsite: string;
  speakerTwitterHandle: string;
  speakerInstagramHandle: string;
  speakerLinkedinUrl: string;
  speakerFacebookUrl: string;
  speakerMastodonHandle: string;
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
  const [formState, { text, textarea, radio, select, checkbox, url, raw }] =
    useFormState<CfpFormFields>(
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

  const {
    loading: conferenceLoading,
    error: conferenceError,
    data: conferenceData,
  } = useCfpFormQuery({
    variables: {
      conference: conferenceCode,
    },
  });

  const { loading: participantDataLoading, data: participantData } =
    useParticipantDataQuery({
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
      speakerWebsite: formState.values.speakerWebsite,
      speakerBio: formState.values.speakerBio,
      speakerTwitterHandle: formState.values.speakerTwitterHandle,
      speakerInstagramHandle: formState.values.speakerInstagramHandle,
      speakerLinkedinUrl: formState.values.speakerLinkedinUrl,
      speakerFacebookUrl: formState.values.speakerFacebookUrl,
      speakerMastodonHandle: formState.values.speakerMastodonHandle,
      speakerPhoto: formState.values.speakerPhoto.split(/[?#]/)[0],
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
    if (!conferenceLoading && submission) {
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
  }, [conferenceLoading]);

  useEffect(() => {
    if (!participantDataLoading && participantData.me.participant) {
      formState.setField("speakerBio", participantData.me.participant.bio);
      formState.setField("speakerPhoto", participantData.me.participant.photo);
      formState.setField(
        "speakerLevel",
        participantData.me.participant.speakerLevel,
      );
      formState.setField(
        "previousTalkVideo",
        participantData.me.participant.previousTalkVideo,
      );
      formState.setField(
        "speakerWebsite",
        participantData.me.participant.website,
      );
      formState.setField(
        "speakerTwitterHandle",
        participantData.me.participant.twitterHandle,
      );
      formState.setField(
        "speakerInstagramHandle",
        participantData.me.participant.instagramHandle,
      );
      formState.setField(
        "speakerLinkedinUrl",
        participantData.me.participant.linkedinUrl,
      );
      formState.setField(
        "speakerFacebookUrl",
        participantData.me.participant.facebookUrl,
      );
      formState.setField(
        "speakerMastodonHandle",
        participantData.me.participant.mastodonHandle,
      );
    }
  }, [participantDataLoading]);

  if (conferenceLoading) {
    return (
      <Alert variant="info">
        <FormattedMessage id="cfp.loading" />
      </Alert>
    );
  }

  if (conferenceError) {
    return <Alert variant="alert">{conferenceError.message}</Alert>;
  }

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
      <Heading mt={5} mb={5} as="h1">
        <FormattedMessage id="cfp.youridea" />
      </Heading>
      <form onSubmit={submitSubmission} sx={{ mb: 4 }}>
        <InputWrapper
          isRequired={true}
          label={<FormattedMessage id="cfp.choosetype" />}
          description={<FormattedMessage id="cfp.choosetypeDescription" />}
        >
          <Flex>
            {conferenceData!.conference.submissionTypes.map((type) => (
              <Label
                key={type.id}
                sx={{
                  width: "auto",
                  mr: 3,
                  fontWeight: "bold",
                }}
              >
                <Radio {...radio("type", type.id)} required={true} />{" "}
                {type.name}
              </Label>
            ))}
          </Flex>
        </InputWrapper>

        <InputWrapper
          as="div"
          isRequired={true}
          label={<FormattedMessage id="cfp.languagesLabel" />}
          description={<FormattedMessage id="cfp.languagesDescription" />}
          errors={getErrors("validationLanguages")}
        >
          <Flex>
            {conferenceData!.conference.languages.map((language) => (
              <Label
                sx={{
                  width: "auto",
                  mr: 3,
                  fontWeight: "bold",
                }}
                key={language.code}
              >
                <Checkbox {...checkbox("languages", language.code)} />
                {language.name}
              </Label>
            ))}
          </Flex>
        </InputWrapper>

        <InputWrapper
          isRequired={true}
          label={<FormattedMessage id="cfp.title" />}
          errors={getErrors("validationTitle")}
        >
          <MultiLingualInput
            {...raw("title")}
            languages={formState.values.languages}
          >
            <Input required={true} maxLength={100} />
          </MultiLingualInput>
        </InputWrapper>

        <Grid
          gap={5}
          sx={{
            gridTemplateColumns: [null, "1fr 1fr"],
          }}
        >
          <Box>
            <InputWrapper
              isRequired={true}
              label={<FormattedMessage id="cfp.elevatorPitchLabel" />}
              description={
                <FormattedMessage id="cfp.elevatorPitchDescription" />
              }
              errors={getErrors("validationElevatorPitch")}
            >
              <MultiLingualInput
                {...raw("elevatorPitch")}
                languages={formState.values.languages}
              >
                <Textarea required={true} maxLength={300} rows={6} />
              </MultiLingualInput>
            </InputWrapper>
          </Box>
          <Box>
            <InputWrapper
              isRequired={true}
              label={<FormattedMessage id="cfp.lengthLabel" />}
              description={<FormattedMessage id="cfp.lengthDescription" />}
              errors={getErrors("validationDuration")}
            >
              <Select {...select("length")} required={true}>
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
              isRequired={true}
              label={<FormattedMessage id="cfp.audienceLevelLabel" />}
              description={
                <FormattedMessage id="cfp.audienceLevelDescription" />
              }
              errors={getErrors("validationAudienceLevel")}
            >
              <Select {...select("audienceLevel")} required={true}>
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
          </Box>
        </Grid>

        <InputWrapper
          isRequired={true}
          label={<FormattedMessage id="cfp.abstractLabel" />}
          description={<FormattedMessage id="cfp.abstractDescription" />}
          errors={getErrors("validationAbstract")}
        >
          <MultiLingualInput
            {...raw("abstract")}
            languages={formState.values.languages}
          >
            <Textarea required={true} maxLength={5000} rows={6} />
          </MultiLingualInput>
        </InputWrapper>

        <InputWrapper
          label={<FormattedMessage id="cfp.notesLabel" />}
          description={<FormattedMessage id="cfp.notesDescription" />}
          errors={getErrors("validationNotes")}
        >
          <Textarea {...textarea("notes")} maxLength={1000} rows={4} />
        </InputWrapper>

        <InputWrapper
          isRequired={true}
          label={<FormattedMessage id="cfp.tagsLabel" />}
          description={<FormattedMessage id="cfp.tagsDescription" />}
          errors={getErrors("validationTags")}
        >
          <TagLine
            tags={formState.values.tags || []}
            onTagChange={(tags: { value: string }[]) => {
              formState.setField(
                "tags",
                tags.map((t) => t.value),
              );
            }}
          />
        </InputWrapper>

        <InputWrapper
          isRequired={false}
          label={<FormattedMessage id="cfp.shortSocialSummaryLabel" />}
          description={
            <FormattedMessage id="cfp.shortSocialSummaryDescription" />
          }
          errors={getErrors("validationShortSocialSummary")}
        >
          <Textarea
            {...textarea("shortSocialSummary")}
            required={false}
            maxLength={128}
            rows={2}
          />
        </InputWrapper>

        <Heading mb={2} as="h2">
          <FormattedMessage id="cfp.aboutYou" />
        </Heading>

        <Text variant="labelDescription" as="p" mb={4}>
          <FormattedMessage id="cfp.aboutYouDescription" />
        </Text>

        {participantDataLoading && (
          <Alert variant="info">
            <FormattedMessage id="global.loading" />
          </Alert>
        )}

        <InputWrapper
          isRequired={true}
          label={<FormattedMessage id="cfp.speakerPhotoLabel" />}
          description={<FormattedMessage id="cfp.speakerPhotoDescription" />}
          errors={getErrors("validationSpeakerPhoto")}
        >
          <FileInput {...raw("speakerPhoto")} />
        </InputWrapper>

        <InputWrapper
          isRequired={true}
          label={<FormattedMessage id="cfp.speakerBioLabel" />}
          description={<FormattedMessage id="cfp.speakerBioDescription" />}
          errors={getErrors("validationSpeakerBio")}
        >
          <Textarea
            {...textarea("speakerBio")}
            required={true}
            maxLength={1000}
            rows={4}
          />
        </InputWrapper>

        <InputWrapper
          label={<FormattedMessage id="cfp.speakerWebsiteLabel" />}
          description={<FormattedMessage id="cfp.speakerWebsiteDescription" />}
          errors={getErrors("validationSpeakerWebsite")}
        >
          <Input {...url("speakerWebsite")} required={false} maxLength={2048} />
        </InputWrapper>

        <InputWrapper
          label={<FormattedMessage id="cfp.socialsLabel" />}
          description={
            <FormattedMessage
              id="cfp.speakerTwitterHandleDescription"
              values={{
                br: <br />,
              }}
            />
          }
          errors={getErrors("validationSpeakerTwitterHandle")}
        >
          <Input
            {...text("speakerTwitterHandle")}
            required={false}
            maxLength={15}
          />
        </InputWrapper>

        <InputWrapper
          description={
            <FormattedMessage
              id="cfp.speakerMastodonHandleDescription"
              values={{
                br: <br />,
              }}
            />
          }
          errors={getErrors("validationSpeakerMastodonHandle")}
        >
          <Input
            {...text("speakerMastodonHandle")}
            required={false}
            maxLength={2048}
          />
        </InputWrapper>

        <InputWrapper
          description={
            <FormattedMessage id="cfp.speakerInstagramHandleDescription" />
          }
          errors={getErrors("validationSpeakerInstagramHandle")}
        >
          <Input
            {...text("speakerInstagramHandle")}
            required={false}
            maxLength={30}
          />
        </InputWrapper>

        <InputWrapper
          description={
            <FormattedMessage id="cfp.speakerLinkedinUrlDescription" />
          }
          errors={getErrors("validationSpeakerLinkedinUrl")}
        >
          <Input
            {...url("speakerLinkedinUrl")}
            required={false}
            maxLength={2048}
          />
        </InputWrapper>

        <InputWrapper
          description={
            <FormattedMessage id="cfp.speakerFacebookUrlDescription" />
          }
          errors={getErrors("validationSpeakerFacebookUrl")}
        >
          <Input
            {...url("speakerFacebookUrl")}
            required={false}
            maxLength={2048}
          />
        </InputWrapper>

        <InputWrapper
          isRequired={true}
          label={<FormattedMessage id="cfp.speakerLevel" />}
          description={<FormattedMessage id="cfp.speakerLevelDescription" />}
          errors={getErrors("validationSpeakerLevel")}
        >
          <Select {...select("speakerLevel")} required={true}>
            {SPEAKER_LEVEL_OPTIONS.map(({ value, disabled, messageId }) => (
              <FormattedMessage id={messageId} key={messageId}>
                {(copy) => (
                  <option disabled={disabled} value={value}>
                    {copy}
                  </option>
                )}
              </FormattedMessage>
            ))}
          </Select>
        </InputWrapper>

        <InputWrapper
          label={<FormattedMessage id="cfp.previousTalkVideo" />}
          description={
            <FormattedMessage id="cfp.previousTalkVideoDescription" />
          }
          errors={getErrors("validationPreviousTalkVideo")}
        >
          <Input
            {...url("previousTalkVideo")}
            required={false}
            maxLength={2048}
          />
        </InputWrapper>

        {getErrors("nonFieldErrors").map((error) => (
          <Alert sx={{ mb: 4 }} variant="alert" key={error}>
            {error}
          </Alert>
        ))}

        {submissionError && (
          <Alert sx={{ mb: 4 }} variant="alert">
            <FormattedMessage
              id="global.tryAgain"
              values={{ error: submissionError.message }}
            />
          </Alert>
        )}

        {submissionData &&
          submissionData.mutationOp.__typename === "Submission" && (
            <Alert sx={{ mb: 4 }} variant="success">
              <FormattedMessage id="cfp.submissionSent" />
            </Alert>
          )}

        {submissionLoading && (
          <Alert variant="info">
            <FormattedMessage id="cfp.loading" />
          </Alert>
        )}

        {hasValidationErrors && (
          <Alert variant="alert">
            <FormattedMessage id="cfp.validationErrors" />
          </Alert>
        )}

        <InputWrapper
          label={<FormattedMessage id="cfp.grantsLabel" />}
          description={
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
                    <FormattedMessage id="cfp.grantsCta" />
                  </Link>
                ),
              }}
            />
          }
        />
        <Button role="secondary">
          <FormattedMessage id="cfp.submit" />
        </Button>
      </form>
    </Fragment>
  );
};
