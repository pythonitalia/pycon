import {
  Button,
  Checkbox,
  Heading,
  Link,
  Page,
  Section,
  Spacer,
  Text,
  Textarea,
  VerticalStack,
} from "@python-italia/pycon-styleguide";
import React, { useCallback, useEffect } from "react";
import { FormattedMessage } from "react-intl";
import { useFormState } from "react-use-form-state";

import type { GetServerSideProps } from "next";

import { addApolloState, getApolloClient } from "~/apollo/client";
import { Alert } from "~/components/alert";
import { createHref } from "~/components/link";
import { PageLoading } from "~/components/page-loading";
import { formatDeadlineDateTime } from "~/helpers/deadlines";
import { prefetchSharedQueries } from "~/helpers/prefetch";
import { useCurrentLanguage } from "~/locale/context";
import NotFoundPage from "~/pages/404";
import {
  Status as GrantStatus,
  StatusOption,
  queryCurrentUser,
  queryGrant,
  queryGrantDeadline,
  useGrantQuery,
  useSendGrantReplyMutation,
} from "~/types";

type GrantReplyFrom = {
  option: StatusOption | null;
};

const APPROVED_STATUSES = [
  GrantStatus.WaitingForConfirmation,
  GrantStatus.Confirmed,
];

// only if the grant is in those of these statuses the User can see the page.
const ALLOWED_STATUSES = [
  GrantStatus.WaitingForConfirmation,
  GrantStatus.Confirmed,
  GrantStatus.Refused,
  GrantStatus.WaitingList,
  GrantStatus.WaitingListMaybe,
];

const ANSWERS_STATUSES = [GrantStatus.Confirmed, GrantStatus.Refused];

const toStatusOption = (status: GrantStatus) => {
  switch (status) {
    case GrantStatus.Confirmed:
      return StatusOption.Confirmed;
    case GrantStatus.Refused:
      return StatusOption.Refused;
  }
};

const GrantReply = () => {
  const language = useCurrentLanguage();
  const code = process.env.conferenceCode;

  const [formState, { radio, text }] = useFormState<GrantReplyFrom>({
    option: null,
  });

  const { loading, error, data } = useGrantQuery({
    variables: {
      conference: code,
    },
  });

  const [
    sendGrantReply,
    { loading: isSubmitting, error: replyError, data: replyData },
  ] = useSendGrantReplyMutation({
    onError(err) {
      console.error(err.message);
    },
  });

  const grant = data?.me?.grant;

  const submitReply = useCallback(
    (e) => {
      e.preventDefault();
      sendGrantReply({
        variables: {
          input: {
            instance: grant?.id,
            status: formState.values.option,
          },
        },
      });
    },
    [formState.values],
  );

  useEffect(() => {
    if (!loading && grant) {
      formState.setField("option", toStatusOption(grant?.status));
    }
  }, [loading]);

  if (loading) {
    return <PageLoading titleId="global.loading" />;
  }

  const hasSentAnswer = ANSWERS_STATUSES.includes(grant?.status) ?? false;

  const answerHasChanged =
    toStatusOption(grant?.status) !== formState.values.option;

  if (error) {
    return (
      <Page>
        <Section>
          <Alert variant="alert">{error.message}</Alert>
        </Section>
      </Page>
    );
  }

  if (
    !error &&
    (data!.me!.grant === null || !ALLOWED_STATUSES.includes(grant.status))
  ) {
    return <NotFoundPage />;
  }

  return (
    <Page>
      <Section>
        <div className="mb-8">
          <Heading>
            <FormattedMessage
              id={
                APPROVED_STATUSES.includes(grant?.status)
                  ? "grants.reply.titleApproved"
                  : "grants.reply.title"
              }
            />
          </Heading>
        </div>
        <div className="mb-8">
          {APPROVED_STATUSES.includes(grant?.status) && (
            <Text>
              <FormattedMessage
                id="grants.reply.descriptionApproved"
                values={{
                  replyDeadline: (
                    <Text size={2} weight="strong">
                      {formatDeadlineDateTime(
                        grant?.applicantReplyDeadline,
                        language,
                      )}
                    </Text>
                  ),
                }}
              />
            </Text>
          )}
        </div>
        <div className="mb-8">
          {hasSentAnswer && (
            <Text>
              <FormattedMessage
                id="grants.reply.currentReply"
                values={{
                  reply: (
                    <Text weight="strong">
                      <FormattedMessage id={`grants.reply.${grant?.status}`} />
                    </Text>
                  ),
                }}
              />
            </Text>
          )}
        </div>

        <form>
          <VerticalStack gap="small">
            {APPROVED_STATUSES.includes(grant?.status) && (
              <label>
                <Checkbox
                  size="small"
                  {...radio("option", StatusOption.Confirmed)}
                />
                <Text as="span">
                  <FormattedMessage id="grants.reply.confirmed" />
                </Text>
              </label>
            )}

            <label>
              <Checkbox
                size="small"
                {...radio("option", GrantStatus.Refused)}
              />
              <Text as="span">
                <FormattedMessage id="grants.reply.refused" />
              </Text>
            </label>
            <Spacer size="medium" />

            <Text size={2}>
              <FormattedMessage
                id="grants.reply.messageDescription"
                values={{
                  visaPageLink: (
                    <Link
                      target="_blank"
                      href={createHref({
                        path: "/visa/",
                        locale: language,
                      })}
                    >
                      <Text
                        decoration="underline"
                        size={2}
                        weight="strong"
                        color="none"
                      >
                        <FormattedMessage id="grants.reply.visaPageLink" />
                      </Text>
                    </Link>
                  ),
                  grantsEmail: (
                    <Link target="_blank" href="mailto:grants@pycon.it">
                      <Text
                        decoration="underline"
                        size={2}
                        weight="strong"
                        color="none"
                      >
                        grants@pycon.it
                      </Text>
                    </Link>
                  ),
                }}
              />
            </Text>
            <Spacer size="small" />
          </VerticalStack>
        </form>

        <Button
          onClick={submitReply}
          disabled={
            !formState.values.option || !answerHasChanged || isSubmitting
          }
        >
          <FormattedMessage id="grants.reply.submitReply" />
        </Button>
        {isSubmitting && (
          <Alert variant="info">
            <FormattedMessage id="grants.reply.sendingReply" />
          </Alert>
        )}
        {!isSubmitting && replyData?.sendGrantReply.__typename === "Grant" && (
          <Alert variant="success">
            <FormattedMessage id="grants.reply.replySentWithSuccess" />
          </Alert>
        )}
        {(replyError ||
          replyData?.sendGrantReply.__typename === "SendGrantReplyError") && (
          <Alert variant="alert">
            <Text>
              {replyError.message || replyData?.sendGrantReply.__typename}
            </Text>
          </Alert>
        )}
      </Section>
    </Page>
  );
};

export const getServerSideProps: GetServerSideProps = async ({
  req,
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

  try {
    await Promise.all([
      prefetchSharedQueries(client, locale),
      queryGrantDeadline(client, {
        conference: process.env.conferenceCode,
      }),
      queryGrant(client, {
        conference: process.env.conferenceCode,
      }),
      queryCurrentUser(client, {
        conference: process.env.conferenceCode,
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

export default GrantReply;
