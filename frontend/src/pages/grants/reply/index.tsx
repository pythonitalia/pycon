import {
  Button,
  Heading,
  Page,
  Section,
  Text,
} from "@python-italia/pycon-styleguide";
import React, { useCallback, useEffect } from "react";
import { FormattedMessage } from "react-intl";
import { useFormState } from "react-use-form-state";
import { Radio, Label, Flex, Textarea } from "theme-ui";

import { GetStaticProps } from "next";
import Error from "next/error";

import { getApolloClient, addApolloState } from "~/apollo/client";
import { Alert } from "~/components/alert";
import { PageLoading } from "~/components/page-loading";
import { formatDeadlineDateTime } from "~/helpers/deadlines";
import { prefetchSharedQueries } from "~/helpers/prefetch";
import { useCurrentLanguage } from "~/locale/context";
import {
  useGrantQuery,
  Status as GrantStatus,
  useSendGrantReplyMutation,
} from "~/types";

type GrantReplyFrom = {
  option: GrantStatus;
  message: string;
};

const APPROVED_STATUSES = [
  GrantStatus.Approved,
  GrantStatus.WaitingForConfirmation,
  GrantStatus.Confirmed,
];

const GrantReply = () => {
  const language = useCurrentLanguage();
  const code = process.env.conferenceCode;

  const [formState, { radio, text }] = useFormState<GrantReplyFrom>({
    option: null,
    message: "",
  });

  const { loading, error, data } = useGrantQuery({
    variables: {
      conference: code,
    },
  });

  const [
    sendGrantReply,
    { loading: isSubmitting, error: replyError, data: replyData },
  ] = useSendGrantReplyMutation({});

  const grant = data && data?.me?.grant;

  const submitReply = useCallback(
    (e) => {
      e.preventDefault();
      console.log("grant.id:", grant);
      sendGrantReply({
        variables: {
          input: {
            instance: grant?.id,
            status: formState.values.option,
            message: formState.values.message,
          },
        },
      });
    },
    [formState.values],
  );

  useEffect(() => {
    if (!loading && grant) {
      formState.setField("option", grant.status);
      formState.setField("message", grant.applicantMessage);
    }
  }, [loading]);

  if (loading) {
    return <PageLoading titleId="global.loading" />;
  }

  const hasSentAnswer =
    grant?.status !== GrantStatus.WaitingForConfirmation ?? false;

  if (error) {
    return (
      <Page>
        <Section>
          <Alert variant="alert">{error.message}</Alert>
        </Section>
      </Page>
    );
  }

  if (!error && data!.me!.grant === null) {
    return <Error statusCode={404} />;
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

        <Flex
          as="form"
          sx={{
            flexDirection: "column",
            gap: 2,
            alignItems: "flex-start",
            mb: 4,
          }}
        >
          {APPROVED_STATUSES.includes(grant?.status) && (
            <Label>
              <Radio {...radio("option", GrantStatus.Confirmed)} />
              <Text as="span">
                <FormattedMessage id="grants.reply.confirmed" />
              </Text>
            </Label>
          )}

          <Label>
            <Radio {...radio("option", GrantStatus.Refused)} />
            <Text as="span">
              <FormattedMessage id="grants.reply.refused" />
            </Text>
          </Label>

          <Label>
            <Radio {...radio("option", GrantStatus.NeedsInfo)} />
            <Text as="span">
              <FormattedMessage id="grants.reply.needs_info" />
            </Text>
          </Label>

          {formState.values.option === GrantStatus.NeedsInfo && (
            <Label>
              <Textarea {...text("message")} rows={5} />
            </Label>
          )}
        </Flex>

        <Button onClick={submitReply} disabled={!formState.values.option}>
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
      </Section>
    </Page>
  );
};

export const getStaticProps: GetStaticProps = async ({ locale }) => {
  const client = getApolloClient();

  await Promise.all([prefetchSharedQueries(client, locale)]);

  return addApolloState(client, {
    props: {},
  });
};

export default GrantReply;
