/** @jsx jsx */

import React, { useCallback, useState } from "react";
import { FormattedMessage } from "react-intl";
import { Box, Heading, Input, jsx, Text } from "theme-ui";

import { useSubscribeMutation } from "~/types";

import { Button } from "../button/button";

const NewsletterForm = () => {
  const [email, setEmail] = useState("");
  const [subscribe, { loading, error, data }] = useSubscribeMutation();

  const canSubmit = email.trim() !== "" && !loading;
  const onSubmit = useCallback(
    async (e) => {
      e.preventDefault();
      if (
        loading ||
        (data &&
          data.subscribeToNewsletter.__typename ===
            "SubscribeToNewsletterErrors")
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
  if (data) {
    return (
      <FormattedMessage id="newsletter.success">
        {(txt) => <Text variant="prefooter">{txt}</Text>}
      </FormattedMessage>
    );
  }
  if (error) {
    return (
      <Box>
        <Text
          color="danger"
          dangerouslySetInnerHTML={{ __html: error.toString() }}
        />
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
            color: "white",
            listStyle: "none",

            a: {
              color: "white",
              textDecoration: "none",
            },
            mb: 3,
          }}
          placeholder="my@email.org"
          onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
            setEmail(e.target.value)
          }
          value={email}
          required={true}
          type="email"
        />
        <Button type="submit" disabled={!canSubmit} loading={loading}>
          <FormattedMessage id="newsletter.button" />
        </Button>
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
