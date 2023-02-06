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
import { prefetchSharedQueries } from "~/helpers/prefetch";
import {
  useGrantQuery,
  Status as GrantStatus,
  useSendGrantReplyMutation,
} from "~/types";

type GrantReplyFrom = {
  option: GrantStatus;
  message: string;
};

const GrantReply = () => {
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
    }
  }, [loading]);

  if (loading) {
    return <PageLoading titleId="global.loading" />;
  }
  console.log({ error, data });

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

  console.log(formState);
  return (
    <Page>
      <Section>
        <div className="mb-8">
          <Heading>
            <FormattedMessage
              id={
                grant?.status === GrantStatus.Approved ||
                grant?.status === GrantStatus.Confirmed
                  ? "grants.reply.titleApproved"
                  : "grants.reply.title"
              }
            />
          </Heading>
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
          {grant?.status === GrantStatus.Approved ||
            (grant?.status === GrantStatus.Confirmed && (
              <Label>
                <Radio {...radio("option", GrantStatus.Confirmed)} />
                <Text as="span">
                  <FormattedMessage id="grants.reply.CONFIRM" />
                </Text>
              </Label>
            ))}

          <Label>
            <Radio {...radio("option", GrantStatus.Refused)} />
            <Text as="span">
              <FormattedMessage id="grants.reply.REFUSE" />
            </Text>
          </Label>

          <Label>
            <Radio {...radio("option", GrantStatus.NeedsInfo)} />
            <Text as="span">
              <FormattedMessage id="grants.reply.NEEDS_INFO" />
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
