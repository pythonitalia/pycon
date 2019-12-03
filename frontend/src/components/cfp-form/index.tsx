/** @jsx jsx */

import { useMutation, useQuery } from "@apollo/react-hooks";
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
import React, { useCallback, useContext } from "react";
import { FormattedMessage } from "react-intl";
import { OptionTypeBase, ValueType } from "react-select";
import { useFormState } from "react-use-form-state";
import { jsx } from "theme-ui";

import { ConferenceContext } from "../../context/conference";
import {
  CfpPageQuery,
  CfpPageQueryVariables,
  SendSubmissionMutation,
  SendSubmissionMutationVariables,
  SubmissionTag,
} from "../../generated/graphql-backend";
import { Alert } from "../alert";
import { TagLine } from "../input-tag";
import { InputWrapper } from "../input-wrapper";
import { Link } from "../link";
import CFP_PAGE_QUERY from "./cfp-page.graphql";
import SEND_SUBMISSION_QUERY from "./send-submission.graphql";

type CfpFormFields = {
  format: string;
  title: string;
  elevatorPitch: string;
  length: number;
  audienceLevel: number;
  abstract: string;
  notes: string;
  topic: string;
  languages: string[];
  tags: string[];
};

export const CfpForm: React.SFC = () => {
  const conferenceCode = useContext(ConferenceContext);
  const {
    loading: conferenceLoading,
    error: conferenceError,
    data: conferenceData,
  } = useQuery<CfpPageQuery, CfpPageQueryVariables>(CFP_PAGE_QUERY, {
    variables: {
      conference: conferenceCode,
    },
  });
  const [
    sendSubmission,
    {
      loading: sendSubmissionLoading,
      error: sendSubmissionError,
      data: sendSubmissionData,
    },
  ] = useMutation<SendSubmissionMutation, SendSubmissionMutationVariables>(
    SEND_SUBMISSION_QUERY,
  );

  const [formState, { text, textarea, radio, select, checkbox }] = useFormState<
    CfpFormFields
  >(
    {},
    {
      withIds: true,
    },
  );

  const onSubmit = useCallback(
    async e => {
      e.preventDefault();

      if (
        sendSubmissionLoading ||
        (sendSubmissionData &&
          sendSubmissionData.sendSubmission.__typename === "Submission")
      ) {
        return;
      }

      sendSubmission({
        variables: {
          input: {
            conference: conferenceCode,
            title: formState.values.title,
            abstract: formState.values.abstract,
            topic: formState.values.topic,
            languages: formState.values.languages,
            type: formState.values.format,
            duration: formState.values.length,
            elevatorPitch: formState.values.elevatorPitch,
            notes: formState.values.notes,
            audienceLevel: formState.values.audienceLevel,
            tags: formState.values.tags,
          },
        },
      });
    },
    [formState, sendSubmissionData, sendSubmissionLoading],
  );

  if (conferenceLoading) {
    return (
      <Box
        sx={{
          maxWidth: "container",
          mx: "auto",
          px: 3,
        }}
      >
        Loading
      </Box>
    );
  }

  if (conferenceError) {
    return (
      <Box
        sx={{
          maxWidth: "container",
          mx: "auto",
          px: 3,
        }}
      >
        Error: {conferenceError.message}
      </Box>
    );
  }

  const getErrors = (
    key:
      | "title"
      | "abstract"
      | "topic"
      | "languages"
      | "type"
      | "duration"
      | "elevatorPitch"
      | "notes"
      | "audienceLevel"
      | "tags"
      | "nonFieldErrors",
  ) =>
    (sendSubmissionData &&
      sendSubmissionData.sendSubmission.__typename === "SendSubmissionErrors" &&
      sendSubmissionData.sendSubmission[key]) ||
    [];

  return (
    <Box
      sx={{
        maxWidth: "container",
        mx: "auto",
        px: 3,
        my: 5,
      }}
    >
      {conferenceData!.me.submissions.length > 0 && (
        <Box sx={{ mb: 5 }}>
          <Text mb={4} as="h1">
            <FormattedMessage id="cfp.yourProposals" />
          </Text>

          <Box as="ul" sx={{ px: 3 }}>
            {conferenceData!.me.submissions.map(submission => (
              <li key={submission.id}>
                <Link href={`/:language/submission/${submission.id}`}>
                  {submission.title}
                </Link>
              </li>
            ))}
          </Box>
        </Box>
      )}

      <Text mb={4} as="h1">
        <FormattedMessage id="cfp.youridea" />
      </Text>
      <Box as="form" onSubmit={onSubmit}>
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
              <Radio {...radio("format", type.id)} required={true} />{" "}
              {type.name}
            </Label>
          ))}
        </Flex>

        <InputWrapper
          sx={{ mb: 5 }}
          label={<FormattedMessage id="cfp.title" />}
          errors={getErrors("title")}
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
              errors={getErrors("elevatorPitch")}
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
              errors={getErrors("topic")}
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
              errors={getErrors("duration")}
            >
              <Select {...select("length")} required={true}>
                <FormattedMessage id="cfp.selectDuration">
                  {txt => (
                    <option value="" disabled={true}>
                      {txt}
                    </option>
                  )}
                </FormattedMessage>
                {conferenceData!.conference.durations
                  .filter(
                    d =>
                      d.allowedSubmissionTypes.findIndex(
                        i => i.id === formState.values.format,
                      ) !== -1,
                  )
                  .map(d => (
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
              errors={getErrors("audienceLevel")}
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
          errors={getErrors("languages")}
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
          errors={getErrors("abstract")}
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
          errors={getErrors("notes")}
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
          errors={getErrors("tags")}
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

        {getErrors("nonFieldErrors").map(error => (
          <Alert sx={{ mb: 4 }} variant="alert" key={error}>
            {error}
          </Alert>
        ))}

        {sendSubmissionError && (
          <Alert sx={{ mb: 4 }} variant="alert">
            <FormattedMessage
              id="cfp.tryAgain"
              values={{ error: sendSubmissionError.message }}
            />
          </Alert>
        )}

        {sendSubmissionData &&
          sendSubmissionData.sendSubmission.__typename === "Submission" && (
            <Alert sx={{ mb: 4 }} variant="success">
              <FormattedMessage id="cfp.submissionSent" />
            </Alert>
          )}

        <Button>
          <FormattedMessage id="cfp.submit" />
        </Button>
      </Box>
    </Box>
  );
};
