import {
  Button,
  Checkbox,
  Heading,
  Page,
  Section,
  Spacer,
  Text,
  Textarea,
  VerticalStack,
} from "@python-italia/pycon-styleguide";
import type { GetServerSideProps } from "next";
import React, { useCallback, useEffect } from "react";
import { FormattedMessage } from "react-intl";
import { useFormState } from "react-use-form-state";

import { useRouter } from "next/router";

import { addApolloState, getApolloClient } from "~/apollo/client";
import { Alert } from "~/components/alert";
import { prefetchSharedQueries } from "~/helpers/prefetch";
import { useTranslatedMessage } from "~/helpers/use-translated-message";
import { useCurrentLanguage } from "~/locale/context";
import type { Language } from "~/locale/languages";
import NotFoundPage from "~/pages/404";
import {
  ScheduleInvitationOption,
  queryGetScheduleInvitation,
  useGetScheduleInvitationQuery,
  useUpdateScheduleInvitationMutation,
} from "~/types";

type SpeakerResponseForm = {
  option: ScheduleInvitationOption;
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
  const { data } = useGetScheduleInvitationQuery({
    variables: {
      submissionId,
      language,
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

  const submitAnswer = useCallback(
    (e) => {
      if (isSubmitting) {
        return;
      }

      if (
        EXTRA_NOTES_OPTIONS.includes(formState.values.option) &&
        !formState.values.notes
      ) {
        return;
      }

      e.preventDefault();
      updateScheduleInvitation({
        variables: {
          input: {
            submissionId,
            option: formState.values.option,
            notes: EXTRA_NOTES_OPTIONS.includes(formState.values.option)
              ? formState.values.notes
              : "",
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
    if (invitation) {
      formState.setField(
        "option",
        hasSentAnswer ? invitation.option : ScheduleInvitationOption.Confirm,
      );
      formState.setField("notes", invitation.notes);
    }
  }, []);

  if (!invitation) {
    return <NotFoundPage />;
  }

  const scheduleDates = invitation.dates.map((date) => ({
    ...date,
    start: formatDateTime(date.start, language),
    end: formatDateTime(date.end, language),
  }));

  const scheduleDate = scheduleDates[0];

  const notesPlaceholder = useTranslatedMessage(
    "schedule.invitation.notes.placeholder",
  );

  return (
    <Page endSeparator={false}>
      <Section>
        <Heading size={1}>
          <FormattedMessage
            id="schedule.invitation.congratulations"
            values={{
              submissionTitle: invitation.title,
            }}
          />
        </Heading>
        <Spacer size="medium" />
        <Text>
          <FormattedMessage
            id="schedule.invitation.program"
            values={{
              date: (
                <strong>
                  <FormattedMessage
                    id="schedule.invitation.date"
                    values={{
                      start: scheduleDate.start,
                      end: scheduleDate.end,
                      duration: scheduleDate.duration,
                    }}
                  />
                </strong>
              ),
            }}
          />
        </Text>
        {scheduleDate.duration !== invitation.submission.duration.duration && (
          <>
            <Spacer size="small" />
            <Text>
              <FormattedMessage
                id="schedule.invitation.durationChanged"
                values={{
                  duration: <strong>{scheduleDate.duration}</strong>,
                  originalDuration: (
                    <strong>{invitation.submission.duration.duration}</strong>
                  ),
                }}
              />
            </Text>
          </>
        )}
        <Spacer size="medium" />
        <Text>
          <FormattedMessage id="schedule.invitation.confirmPresence" />
        </Text>
        <Spacer size="medium" />

        {hasSentAnswer && (
          <Text>
            <FormattedMessage
              id="schedule.invitation.currentAnswer"
              values={{
                answer: (
                  <Text as="span" weight="strong">
                    <FormattedMessage
                      id={`schedule.invitation.presence.${invitation.option}`}
                    />
                  </Text>
                ),
              }}
            />
          </Text>
        )}
        <form>
          <VerticalStack gap="small" alignItems="start">
            <label className="flex gap-2">
              <Checkbox
                size="small"
                {...radio("option", ScheduleInvitationOption.Confirm)}
              />
              <Text as="span">
                <FormattedMessage id="schedule.invitation.presence.CONFIRM" />
              </Text>
            </label>

            <label className="flex gap-2">
              <Checkbox
                size="small"
                {...radio("option", ScheduleInvitationOption.Reject)}
              />
              <Text as="span">
                <FormattedMessage id="schedule.invitation.presence.REJECT" />
              </Text>
            </label>

            <label className="flex gap-2">
              <Checkbox
                size="small"
                {...radio("option", ScheduleInvitationOption.CantAttend)}
              />
              <Text as="span">
                <FormattedMessage id="schedule.invitation.presence.CANT_ATTEND" />
              </Text>
            </label>

            {EXTRA_NOTES_OPTIONS.includes(formState.values.option) && (
              <label className="flex flex-col">
                <Text as="p">
                  <FormattedMessage id="schedule.invitation.presence.notes" />
                </Text>
                <Spacer size="small" />
                <Textarea
                  {...text("notes")}
                  placeholder={notesPlaceholder}
                  rows={4}
                />
              </label>
            )}

            <Button
              variant="secondary"
              onClick={submitAnswer}
              disabled={
                EXTRA_NOTES_OPTIONS.includes(formState.values.option) &&
                !formState.values.notes
              }
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
                "ScheduleInvitation" && (
                <Alert variant="success">
                  <FormattedMessage id="schedule.invitation.answerSentWithSuccess" />
                </Alert>
              )}
            {!isSubmitting &&
              submitAnswerData?.updateScheduleInvitation.__typename ===
                "ScheduleInvitationNotFound" && (
                <Alert variant="alert">
                  <FormattedMessage id="schedule.invitation.unableToFindInvitation" />
                </Alert>
              )}
          </VerticalStack>
        </form>
      </Section>
    </Page>
  );
};

export const getServerSideProps: GetServerSideProps = async ({
  req,
  params,
  locale,
}) => {
  const identityToken = req.cookies.pythonitalia_sessionid;
  if (!identityToken) {
    return {
      redirect: {
        destination: "/login",
        permanent: false,
      },
    };
  }

  const client = getApolloClient(null, req.cookies);
  const submissionId = params?.submissionId as string;

  try {
    await Promise.all([
      prefetchSharedQueries(client, locale),
      queryGetScheduleInvitation(client, {
        language: locale,
        submissionId,
      }),
    ]);
  } catch (e) {
    return {
      redirect: {
        destination: "/login",
        permanent: false,
      },
    };
  }

  return addApolloState(
    client,
    {
      props: {},
    },
    null,
  );
};

export default Invitation;
