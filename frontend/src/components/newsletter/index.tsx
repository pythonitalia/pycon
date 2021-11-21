/** @jsxRuntime classic */

/** @jsx jsx */
import React, { useCallback, useState } from "react";
import { FormattedMessage } from "react-intl";
import { Box, Heading, Input, jsx, Text } from "theme-ui";

import { Alert } from "~/components/alert";
import { NewsletterSubscriptionResult, useSubscribeMutation } from "~/types";

import { Button } from "../button/button";
import { ErrorsList } from "../errors-list";

const NewsletterForm = () => {
  const [email, setEmail] = useState("");
  const [subscribe, { loading, error, data }] = useSubscribeMutation();

  const canSubmit = email.trim() !== "" && !loading;
  const onSubmit = useCallback(
    async (e) => {
      e.preventDefault();
      if (
        loading ||
        data?.subscribeToNewsletter.__typename === "NewsletterSubscribeResult"
      ) {
        return;
      }
      subscribe({
        variables: {
          email,
        },
      });
    },
    [email],
  );
  const getErrors = (key: "validationEmail" | "nonFieldErrors") =>
    (data?.subscribeToNewsletter?.__typename ===
      "SubscribeToNewsletterErrors" &&
      data.subscribeToNewsletter[key]) ||
    [];

  const unableToSubscribe =
    data?.subscribeToNewsletter.__typename == "NewsletterSubscribeResult" &&
    data?.subscribeToNewsletter.status ===
      NewsletterSubscriptionResult.UnableToSubscribe;

  if (
    data?.subscribeToNewsletter.__typename == "NewsletterSubscribeResult" &&
    !unableToSubscribe
  ) {
    const success =
      data?.subscribeToNewsletter.status ==
      NewsletterSubscriptionResult.Subscribed;
    return (
      <Box>
        <FormattedMessage id="newsletter.text">
          {(txt) => (
            <Text variant="prefooter" mb={3}>
              {txt}
            </Text>
          )}
        </FormattedMessage>

        <FormattedMessage
          id={success ? "newsletter.success" : "newsletter.confirmViaEmail"}
        >
          {(txt) => (
            <Text sx={{ color: "green", fontWeight: "bold" }}>{txt}</Text>
          )}
        </FormattedMessage>
      </Box>
    );
  }

  return (
    <Box as="form" onSubmit={onSubmit}>
      <Box>
        <FormattedMessage id="newsletter.text">
          {(txt) => (
            <Text variant="prefooter" mb={3}>
              {txt}
            </Text>
          )}
        </FormattedMessage>
        <Input
          sx={{
            listStyle: "none",
            mb: 3,
          }}
          placeholder="guido@python.org"
          onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
            setEmail(e.target.value)
          }
          value={email}
          required={true}
          type="email"
        />
        <ErrorsList sx={{ mb: 4 }} errors={getErrors("validationEmail")} />

        <Button type="submit" disabled={!canSubmit} loading={loading}>
          <FormattedMessage id="newsletter.button" />
        </Button>

        {(error || unableToSubscribe) && (
          <Alert variant="alert">
            <FormattedMessage id="newsletter.error" />
          </Alert>
        )}
      </Box>
    </Box>
  );
};

export const NewsletterSection: React.SFC = () => (
  <Box>
    <FormattedMessage id="newsletter.header">
      {(txt) => <Heading sx={{ fontSize: 5, mb: 4 }}>{txt}</Heading>}
    </FormattedMessage>
    <NewsletterForm />
  </Box>
);
