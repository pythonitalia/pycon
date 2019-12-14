/** @jsx jsx */

import { useQuery } from "@apollo/react-hooks";
import {
  Box,
  Button,
  Checkbox,
  Flex,
  Grid,
  Input,
  Label,
  Radio,
  Select,
  Text,
  Textarea,
} from "@theme-ui/components";
import { ApolloError } from "apollo-client";
import React, { Fragment, useEffect } from "react";
import { FormattedMessage } from "react-intl";
import { useFormState } from "react-use-form-state";
import { jsx } from "theme-ui";

import {
  CfpFormQuery,
  CfpFormQueryVariables,
  SendSubmissionMutation,
  UpdateSubmissionMutation,
} from "../../generated/graphql-backend";
import { Alert } from "../alert";
import { TagLine } from "../input-tag";
import { InputWrapper } from "../input-wrapper";
import CFP_FORM_QUERY from "./cfp-form.graphql";

export type CfpFormFields = {
  type: string;
  title: string;
  elevatorPitch: string;
  length: string;
  audienceLevel: string;
  abstract: string;
  notes: string;
  topic: string;
  languages: string[];
  tags: string[];
  speakerLevel: string;
  previousTalkVideo: string;
};

type SubmissionStructure = {
  type: { id: string };
  title: string;
  elevatorPitch: string;
  topic: { id: string };
  duration: { id: string };
  audienceLevel: { id: string };
  languages: { code: string }[];
  abstract: string;
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
  data: SendSubmissionMutation | UpdateSubmissionMutation | undefined;
};

export const CfpForm: React.SFC<Props> = ({
  onSubmit,
  conferenceCode,
  submission,
  loading: submissionLoading,
  error: submissionError,
  data: submissionData,
}) => {
  const [formState, { text, textarea, radio, select, checkbox }] = useFormState<
    CfpFormFields
  >(
    {},
    {
      withIds: true,
    },
  );

  const setupCleanForm = (data: CfpFormQuery) => {
    const submissionTypes = data.conference.submissionTypes;

    if (submissionTypes.length === 0) {
      return;
    }

    const type = submissionTypes[0].id;
    formState.setField("type", type);

    const durations = data.conference.durations;

    if (durations.length > 0) {
      // Check if we have a valid duration to preselect that is also allowed
      // in the type we automatically selected
      const validDurations = durations.filter(
        d => d.allowedSubmissionTypes.findIndex(t => t.id === type) !== -1,
      );

      if (validDurations.length > 0) {
        formState.setField("length", validDurations[0].id);
      }
    }

    if (data.conference.topics.length > 0) {
      formState.setField("topic", data.conference.topics[0].id);
    }

    if (data.conference.audienceLevels.length > 0) {
      formState.setField("audienceLevel", data.conference.audienceLevels[0].id);
    }
  };

  const setupFormFromSubmission = (_: CfpFormQuery) => {
    formState.setField("type", submission!.type.id);
    formState.setField("title", submission!.title);
    formState.setField("elevatorPitch", submission!.elevatorPitch);
    formState.setField("topic", submission!.topic.id);
    formState.setField("length", submission!.duration.id);
    formState.setField("audienceLevel", submission!.audienceLevel.id);
    formState.setField(
      "languages",
      submission!.languages.map(l => l.code),
    );
    formState.setField("abstract", submission!.abstract);
    formState.setField("notes", submission!.notes);
    formState.setField(
      "tags",
      submission!.tags.map(t => t.id),
    );
    formState.setField("speakerLevel", submission!.speakerLevel);
    formState.setField("previousTalkVideo", submission!.previousTalkVideo);
  };

  const {
    loading: conferenceLoading,
    error: conferenceError,
    data: conferenceData,
  } = useQuery<CfpFormQuery, CfpFormQueryVariables>(CFP_FORM_QUERY, {
    variables: {
      conference: conferenceCode,
    },
    onCompleted(data) {
      if (submission) {
        setupFormFromSubmission(data);
      } else {
        setupCleanForm(data);
      }
    },
  });

  const submitSubmission = async (e: React.MouseEvent) => {
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
    d =>
      d.allowedSubmissionTypes.findIndex(
        i => i.id === formState.values.type,
      ) !== -1,
  );

  useEffect(() => {
    if (!allowedDurations?.length) {
      return;
    }

    // When changing format we need to reset to the first
    // available duration of the new format
    formState.setField("length", allowedDurations[0].id);
  }, [formState.values.type]);

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
      <Text mb={4} as="h1">
        <FormattedMessage id="cfp.youridea" />
      </Text>
      <Box as="form" onSubmit={submitSubmission}>
        <Label mb={3} htmlFor="type">
          <FormattedMessage id="cfp.choosetype" />
        </Label>

        <Flex mb={5}>
          {conferenceData!.conference.submissionTypes.map(type => (
            <Label
              key={type.id}
              sx={{
                width: "auto",
                marginRight: 3,
                color: "green",
                fontWeight: "bold",
              }}
            >
              <Radio {...radio("type", type.id)} required={true} /> {type.name}
            </Label>
          ))}
        </Flex>

        <InputWrapper
          sx={{ mb: 5 }}
          label={<FormattedMessage id="cfp.title" />}
          errors={getErrors("validationTitle")}
        >
          <Input {...text("title")} required={true} />
        </InputWrapper>

        <Grid
          sx={{
            mb: 5,
            gridColumnGap: 5,
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
              <Textarea
                sx={{
                  resize: "vertical",
                  minHeight: 340,
                }}
                {...textarea("elevatorPitch")}
                maxLength="300"
                rows="6"
              />
            </InputWrapper>
          </Box>
          <Box>
            <InputWrapper
              label={<FormattedMessage id="cfp.topicLabel" />}
              description={<FormattedMessage id="cfp.topicDescription" />}
              errors={getErrors("validationTopic")}
            >
              <Select {...select("topic")} required={true}>
                <FormattedMessage id="cfp.selectTopic">
                  {txt => (
                    <option value="" disabled={true}>
                      {txt}
                    </option>
                  )}
                </FormattedMessage>
                {conferenceData!.conference.topics.map(d => (
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
                  {txt => (
                    <option value="" disabled={true}>
                      {txt}
                    </option>
                  )}
                </FormattedMessage>
                {allowedDurations!.map(d => (
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
                  {txt => (
                    <option value="" disabled={true}>
                      {txt}
                    </option>
                  )}
                </FormattedMessage>
                {conferenceData!.conference.audienceLevels.map(a => (
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
          label={<FormattedMessage id="cfp.languagesLabel" />}
          description={<FormattedMessage id="cfp.languagesDescription" />}
          errors={getErrors("validationLanguages")}
        >
          {conferenceData!.conference.languages.map(language => (
            <Label
              key={language.code}
              sx={{
                mt: 3,
              }}
            >
              <Checkbox {...checkbox("languages", language.code)} />
              {language.name}
            </Label>
          ))}
        </InputWrapper>

        <InputWrapper
          sx={{
            mb: 5,
          }}
          label={<FormattedMessage id="cfp.abstractLabel" />}
          description={<FormattedMessage id="cfp.abstractDescription" />}
          errors={getErrors("validationAbstract")}
        >
          <Textarea
            sx={{
              resize: "vertical",
              minHeight: 200,
            }}
            {...textarea("abstract")}
            rows="6"
          />
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
            rows="4"
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
                tags.map(t => t.value),
              );
            }}
          />
        </InputWrapper>

        <Text mb={2} as="h2">
          <FormattedMessage id="cfp.aboutYou" />
        </Text>

        <Text variant="labelDescription" as="p" mb={4}>
          <FormattedMessage id="cfp.aboutYouDescription" />
        </Text>

        <InputWrapper
          label={<FormattedMessage id="cfp.speakerLevel" />}
          description={<FormattedMessage id="cfp.speakerLevelDescription" />}
          errors={getErrors("validationSpeakerLevel")}
        >
          <Select {...select("speakerLevel")} required={true}>
            <FormattedMessage id="cfp.speakerLevel.new">
              {copy => <option value="new">{copy}</option>}
            </FormattedMessage>

            <FormattedMessage id="cfp.speakerLevel.intermediate">
              {copy => <option value="intermediate">{copy}</option>}
            </FormattedMessage>

            <FormattedMessage id="cfp.speakerLevel.experienced">
              {copy => <option value="experienced">{copy}</option>}
            </FormattedMessage>
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

        {getErrors("nonFieldErrors").map(error => (
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

        <Button>
          <FormattedMessage id="cfp.submit" />
        </Button>
      </Box>
    </Fragment>
  );
};
