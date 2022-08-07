/** @jsxRuntime classic */

/** @jsx jsx */
import { ApolloError } from "@apollo/client";
import React, { Fragment, useEffect } from "react";
import { FormattedMessage } from "react-intl";
import { useFormState } from "react-use-form-state";
import {
  Box,
  Checkbox,
  Flex,
  Grid,
  Input,
  jsx,
  Label,
  Radio,
  Select,
  Text,
  Textarea,
  Heading,
} from "theme-ui";

import {
  SendSubmissionMutation,
  UpdateSubmissionMutation,
  useCfpFormQuery,
} from "~/types";

import { Alert } from "../alert";
import { Button } from "../button/button";
import { TagLine } from "../input-tag";
import { InputWrapper } from "../input-wrapper";
import { MultiLingualInput } from "../multilingual-input";

export type CfpFormFields = {
  type: string;
  title: { it: string; en: string };
  elevatorPitch: { it: string; en: string };
  length: string;
  audienceLevel: string;
  abstract: { it: string; en: string };
  notes: string;
  topic: string;
  languages: string[];
  tags: string[];
  speakerLevel: string;
  previousTalkVideo: string;
};

export type SubmissionStructure = {
  type: { id: string };
  title: { it: string; en: string };
  elevatorPitch: { it: string; en: string };
  topic: { id: string };
  duration: { id: string };
  audienceLevel: { id: string };
  languages: { code: string }[];
  abstract: { it: string; en: string };
  notes: string;
  previousTalkVideo: string;
  speakerLevel: string;
  tags: { id: string }[];
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

export const CfpForm = ({
  onSubmit,
  conferenceCode,
  submission,
  loading: submissionLoading,
  error: submissionError,
  data: submissionData,
}: Props) => {
  const [formState, { text, textarea, radio, select, checkbox, raw }] =
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

  const submitSubmission = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    onSubmit({
      title: formState.values.title,
      abstract: formState.values.abstract,
      topic: formState.values.topic,
      languages: formState.values.languages,
      type: formState.values.type,
      length: formState.values.length,
      elevatorPitch: formState.values.elevatorPitch,
      notes: formState.values.notes,
      audienceLevel: formState.values.audienceLevel,
      tags: formState.values.tags,
      speakerLevel: formState.values.speakerLevel,
      previousTalkVideo: formState.values.previousTalkVideo,
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
      formState.setField("title", submission!.title);
      formState.setField("elevatorPitch", submission!.elevatorPitch);
      formState.setField("topic", submission!.topic.id);
      formState.setField("length", submission!.duration.id);
      formState.setField("audienceLevel", submission!.audienceLevel.id);
      formState.setField(
        "languages",
        submission!.languages.map((l) => l.code),
      );
      formState.setField("abstract", submission!.abstract);
      formState.setField("notes", submission!.notes);
      formState.setField(
        "tags",
        submission!.tags.map((t) => t.id),
      );
      formState.setField("speakerLevel", submission!.speakerLevel);
      formState.setField("previousTalkVideo", submission!.previousTalkVideo);
    }
  }, [conferenceLoading]);

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
    submissionData?.mutationOp.__typename === "SendSubmissionErrors" ||
    submissionData?.mutationOp.__typename === "UpdateSubmissionErrors";

  /* todo refactor to avoid multiple __typename? */
  const getErrors = (
    key:
      | "validationTitle"
      | "validationAbstract"
      | "validationTopic"
      | "validationLanguages"
      | "validationType"
      | "validationDuration"
      | "validationElevatorPitch"
      | "validationNotes"
      | "validationAudienceLevel"
      | "validationTags"
      | "validationSpeakerLevel"
      | "validationPreviousTalkVideo"
      | "nonFieldErrors",
  ): string[] =>
    ((submissionData?.mutationOp.__typename === "SendSubmissionErrors" ||
      submissionData?.mutationOp.__typename === "UpdateSubmissionErrors") &&
      submissionData!.mutationOp[key]) ||
    [];

  return (
    <Fragment>
      <Heading mt={5} mb={5} as="h1">
        <FormattedMessage id="cfp.youridea" />
      </Heading>
      <form onSubmit={submitSubmission} sx={{ mb: 4 }}>
        <InputWrapper
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
          sx={{ mb: 5 }}
          label={<FormattedMessage id="cfp.title" />}
          errors={getErrors("validationTitle")}
        >
          <MultiLingualInput
            {...raw("title")}
            languages={formState.values.languages}
          >
            <Input required={true} />
          </MultiLingualInput>
        </InputWrapper>

        <Grid
          gap={5}
          sx={{
            mb: 5,
            gridTemplateColumns: [null, "1fr 1fr"],
          }}
        >
          <Box>
            <InputWrapper
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
                <Textarea
                  sx={{
                    resize: "vertical",
                    minHeight: 340,
                  }}
                  maxLength={300}
                  rows={6}
                />
              </MultiLingualInput>
            </InputWrapper>
          </Box>
          <Box>
            <InputWrapper
              label={<FormattedMessage id="cfp.trackLabel" />}
              description={<FormattedMessage id="cfp.topicDescription" />}
              errors={getErrors("validationTopic")}
            >
              <Select {...select("topic")} required={true}>
                <FormattedMessage id="cfp.selectTrack">
                  {(txt) => (
                    <option value="" disabled={true}>
                      {txt}
                    </option>
                  )}
                </FormattedMessage>
                {conferenceData!.conference.topics.map((d) => (
                  <option key={d.id} value={d.id}>
                    {d.name}
                  </option>
                ))}
              </Select>
            </InputWrapper>

            <InputWrapper
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
          sx={{
            mb: 5,
          }}
          label={<FormattedMessage id="cfp.abstractLabel" />}
          description={<FormattedMessage id="cfp.abstractDescription" />}
          errors={getErrors("validationAbstract")}
        >
          <MultiLingualInput
            {...raw("abstract")}
            languages={formState.values.languages}
          >
            <Textarea
              sx={{
                resize: "vertical",
                minHeight: 200,
              }}
              rows={6}
            />
          </MultiLingualInput>
        </InputWrapper>

        <InputWrapper
          label={<FormattedMessage id="cfp.notesLabel" />}
          description={<FormattedMessage id="cfp.notesDescription" />}
          errors={getErrors("validationNotes")}
        >
          <Textarea
            sx={{
              resize: "vertical",
              minHeight: 150,
            }}
            {...textarea("notes")}
            rows={4}
          />
        </InputWrapper>

        <InputWrapper
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

        <Heading mb={2} as="h2">
          <FormattedMessage id="cfp.aboutYou" />
        </Heading>

        <Text variant="labelDescription" as="p" mb={4}>
          <FormattedMessage id="cfp.aboutYouDescription" />
        </Text>

        <InputWrapper
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
          <Input {...text("previousTalkVideo")} required={false} />
        </InputWrapper>

        {getErrors("nonFieldErrors").map((error) => (
          <Alert sx={{ mb: 4 }} variant="alert" key={error}>
            {error}
          </Alert>
        ))}

        {submissionError && (
          <Alert sx={{ mb: 4 }} variant="alert">
            <FormattedMessage
              id="cfp.tryAgain"
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

        <Button loading={submissionLoading}>
          <FormattedMessage id="cfp.submit" />
        </Button>
      </form>
    </Fragment>
  );
};
