/** @jsxRuntime classic */

/** @jsx jsx */
import React, { useCallback, useEffect } from "react";
import { FormattedMessage } from "react-intl";
import { useFormState } from "react-use-form-state";
import {
  Flex,
  Box,
  jsx,
  Heading,
  Text,
  Button,
  Textarea,
  Label,
  Radio,
} from "theme-ui";

import { GetStaticPaths, GetStaticProps } from "next";
import { useRouter } from "next/router";

import { getApolloClient, addApolloState } from "~/apollo/client";
import { Alert } from "~/components/alert";
import { prefetchSharedQueries } from "~/helpers/prefetch";
import { useCurrentLanguage } from "~/locale/context";
import { Language } from "~/locale/languages";
import {
  ScheduleInvitationOption,
  useGetScheduleInvitationQuery,
  useUpdateScheduleInvitationMutation,
} from "~/types";

type SpeakerResponseForm = {
  option: string;
  notes: string;
};

const EXTRA_NOTES_OPTIONS = [
  ScheduleInvitationOption.Maybe,
  ScheduleInvitationOption.Reject,
];

const formatDateTime = (datetime: string, language: Language) => {
  const d = new Date(datetime);

  const formatter = new Intl.DateTimeFormat(language, {
    year: "numeric",
    month: "long",
    day: "numeric",
    hour: "numeric",
    minute: "numeric",
  });

  return formatter.format(d);
};

const Invitation = () => {
  const language = useCurrentLanguage();
  const router = useRouter();
  const submissionId = router.query.submissionId as string;
  const { loading, data, error } = useGetScheduleInvitationQuery({
    variables: {
      submissionId,
    },
  });
  const [
    updateScheduleInvitation,
    { loading: isSubmitting, data: submitAnswerData },
  ] = useUpdateScheduleInvitationMutation();
  const [formState, { radio, text }] = useFormState<SpeakerResponseForm>({
    option: ScheduleInvitationOption.Confirm,
    notes: "",
  });

  console.log("submissionId", submissionId);
  const submitAnswer = useCallback(
    (e) => {
      if (isSubmitting) {
        return;
      }
      e.preventDefault();
      updateScheduleInvitation({
        variables: {
          input: {
            submissionId,
            option: formState.values.option,
            notes: formState.values.notes,
          },
        },
      });
    },
    [formState.values, submissionId, isSubmitting],
  );

  const invitation = data?.scheduleInvitation;
  const hasSentAnswer =
    invitation?.option !== ScheduleInvitationOption.NoAnswer ?? false;

  useEffect(() => {
    if (!loading && invitation) {
      formState.setField(
        "option",
        hasSentAnswer ? invitation.option : ScheduleInvitationOption.Confirm,
      );
      formState.setField("notes", invitation.notes);
    }
  }, [loading]);

  if (loading) {
    return (
      <Box sx={{ borderTop: "primary" }}>
        <Box sx={{ maxWidth: "largeContainer", p: 3, mx: "auto" }}>
          <FormattedMessage id="schedule.invitation.wait" />
        </Box>
      </Box>
    );
  }

  console.log("data", data, "error", error);

  if (!invitation) {
    return (
      <Box sx={{ borderTop: "primary" }}>
        <Box sx={{ maxWidth: "largeContainer", p: 3, mx: "auto" }}>
          <FormattedMessage id="schedule.invitation.invitationNotValid" />
        </Box>
      </Box>
    );
  }

  const scheduleDates = invitation.dates.map((date) => ({
    ...date,
    start: formatDateTime(date.start, language),
    end: formatDateTime(date.end, language),
  }));

  return (
    <Box sx={{ borderTop: "primary" }}>
      <Box sx={{ maxWidth: "largeContainer", p: 3, mx: "auto" }}>
        <Heading>
          <FormattedMessage
            id="schedule.invitation.congratulations"
            values={{
              submissionTitle: invitation.submission.title,
            }}
          />
        </Heading>
        <Text
          sx={{
            mt: 2,
          }}
        >
          <FormattedMessage id="schedule.invitation.program" />
        </Text>
        <ul
          sx={{
            listStyle: "none",
          }}
        >
          {scheduleDates.map((date) => (
            <li>
              <Text>
                <FormattedMessage
                  id="schedule.invitation.date"
                  values={{
                    start: date.start,
                    end: date.end,
                  }}
                />
              </Text>
            </li>
          ))}
        </ul>
        <Text
          sx={{
            mt: 2,
          }}
        >
          <FormattedMessage id="schedule.invitation.confirmPresence" />
        </Text>
        {hasSentAnswer && (
          <Text
            sx={{
              mt: 2,
            }}
          >
            <FormattedMessage
              id="schedule.invitation.currentAnswer"
              values={{
                answer: (
                  <Text
                    as="span"
                    sx={{
                      fontWeight: "bold",
                    }}
                  >
                    <FormattedMessage
                      id={`schedule.invitation.presence.${invitation.option}`}
                    />
                  </Text>
                ),
              }}
            />
          </Text>
        )}
        <Flex
          as="form"
          sx={{
            flexDirection: "column",
            mt: 2,
            gap: 2,
            alignItems: "flex-start",
          }}
        >
          <Label>
            <Radio {...radio("option", ScheduleInvitationOption.Confirm)} />
            <Text as="span">
              <FormattedMessage id="schedule.invitation.presence.CONFIRM" />
            </Text>
          </Label>

          <Label>
            <Radio {...radio("option", ScheduleInvitationOption.Maybe)} />
            <Text as="span">
              <FormattedMessage id="schedule.invitation.presence.MAYBE" />
            </Text>
          </Label>

          <Label>
            <Radio {...radio("option", ScheduleInvitationOption.Reject)} />
            <Text as="span">
              <FormattedMessage id="schedule.invitation.presence.REJECT" />
            </Text>
          </Label>

          <Label>
            <Radio {...radio("option", ScheduleInvitationOption.CantAttend)} />
            <Text as="span">
              <FormattedMessage id="schedule.invitation.presence.CANT_ATTEND" />
            </Text>
          </Label>

          {EXTRA_NOTES_OPTIONS.includes(formState.values.option) && (
            <Label
              sx={{
                flexDirection: "column",
              }}
            >
              <Text as="p">
                <FormattedMessage id="schedule.invitation.presence.notes" />
              </Text>

              <Textarea {...text("notes")} />
            </Label>
          )}

          <Button
            sx={{
              display: "block",
            }}
            onClick={submitAnswer}
          >
            <FormattedMessage id="schedule.invitation.submitAnswer" />
          </Button>
          {isSubmitting && (
            <Alert variant="info">
              <FormattedMessage id="schedule.invitation.sendingAnswer" />
            </Alert>
          )}
          {!isSubmitting &&
            submitAnswerData?.updateScheduleInvitation.__typename ===
              "OperationResult" && (
              <Alert variant="success">
                <FormattedMessage id="schedule.invitation.answerSentWithSuccess" />
              </Alert>
            )}
          {!isSubmitting &&
            submitAnswerData?.updateScheduleInvitation.__typename ===
              "ScheduleInvitationNotFound" && (
              <Alert variant="error">
                <FormattedMessage id="schedule.invitation.unableToFindInvitation" />
              </Alert>
            )}
        </Flex>
      </Box>
    </Box>
  );
};

export const getStaticProps: GetStaticProps = async ({ locale }) => {
  const client = getApolloClient();

  await Promise.all([prefetchSharedQueries(client, locale)]);

  return addApolloState(client, {
    props: {},
  });
};

export const getStaticPaths: GetStaticPaths = async () => {
  return {
    paths: [],
    fallback: "blocking",
  };
};

export default Invitation;
