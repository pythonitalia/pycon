/** @jsxRuntime classic */

/** @jsx jsx */
import { Button, Spacer, Text } from "@python-italia/pycon-styleguide";
import React, { useCallback, useState } from "react";
import { FormattedMessage } from "react-intl";
import { Box, Input, jsx } from "theme-ui";

import { Alert } from "~/components/alert";
import { NewsletterSubscriptionResult, useSubscribeMutation } from "~/types";

import { ErrorsList } from "../errors-list";

const NewsletterForm = () => {
  const [email, setEmail] = useState("");
  const [subscribe, { loading, error, data }] = useSubscribeMutation();
  const subscribeToNewsletter = data?.subscribeToNewsletter;

  const hasFormErrors =
    subscribeToNewsletter?.__typename === "SubscribeToNewsletterErrors";
  const hasCompletedSubscription =
    subscribeToNewsletter?.__typename === "NewsletterSubscribeResult";
  const isUnableToSubscribe =
    hasCompletedSubscription &&
    subscribeToNewsletter?.status ===
      NewsletterSubscriptionResult.UnableToSubscribe;

  const canSubmit = email.trim() !== "" && !loading;
  const onSubmit = useCallback(
    async (e) => {
      e.preventDefault();

      if (loading || hasCompletedSubscription) {
        return;
      }

      subscribe({
        variables: {
          email,
        },
      });
    },
    [email, hasCompletedSubscription, loading],
  );

  const getErrors = (key: "validationEmail" | "nonFieldErrors") =>
    (hasFormErrors && data.subscribeToNewsletter[key]) || [];

  if (hasCompletedSubscription && !isUnableToSubscribe) {
    const success =
      subscribeToNewsletter.status == NewsletterSubscriptionResult.Subscribed;

    return (
      <Box>
        <Text size={2}>
          <FormattedMessage id="newsletter.text" />
        </Text>

        <Spacer size="medium" />

        <Text size={2}>
          <FormattedMessage
            id={success ? "newsletter.success" : "newsletter.confirmViaEmail"}
          />
        </Text>
      </Box>
    );
  }

  return (
    <Box as="form" onSubmit={onSubmit}>
      <Box>
        <Text size={2}>
          <FormattedMessage id="newsletter.text" />
        </Text>
        <Spacer size="medium" />
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

        <Button role="secondary" disabled={!canSubmit}>
          <FormattedMessage id="newsletter.button" />
        </Button>

        {(error || isUnableToSubscribe) && (
          <Alert variant="alert">
            <FormattedMessage id="newsletter.error" />
          </Alert>
        )}
      </Box>
    </Box>
  );
};

export const NewsletterSection = () => <NewsletterForm />;
