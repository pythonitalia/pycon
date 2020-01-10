/** @jsx jsx */
import { useMutation } from "@apollo/react-hooks";
import { Box, Button, Heading, Input, Text } from "@theme-ui/components";
import { useCallback, useState } from "react";
import { FormattedMessage } from "react-intl";
import { jsx } from "theme-ui";

import {
  SubscribeMutation,
  SubscribeMutationVariables,
} from "../../generated/graphql-backend";
import SUBSCRIBE_QUERY from "./subscribe.graphql";

const NewsletterForm = () => {
  const [email, setEmail] = useState("");
  const [subscribe, { loading, error, data }] = useMutation<
    SubscribeMutation,
    SubscribeMutationVariables
  >(SUBSCRIBE_QUERY);

  const canSubmit = email.trim() !== "" && !loading;
  const onSubmit = useCallback(
    async e => {
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
    console.log(data);
    return (
      <FormattedMessage id="newsletter.success">
        {txt => <Text variant="prefooter">{txt}</Text>}
      </FormattedMessage>
    );
  }
  if (error) {
    console.log(error);
    return (
      <Box>
        <Text
          color="danger"
          use="strong"
          dangerouslySetInnerHTML={{ __html: error }}
        />
      </Box>
    );
  }

  return (
    <Box as="form" onSubmit={onSubmit}>
      <Box>
        <FormattedMessage id="newsletter.text">
          {txt => (
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
          onChange={e => setEmail(e.target.value)}
          value={email}
          isRequired={true}
          type="email"
        />
        <Button type="submit" disabled={!canSubmit} isLoading={loading}>
          <FormattedMessage id="newsletter.button" />
        </Button>
      </Box>
    </Box>
  );
};

export const NewsletterSection: React.SFC = () => (
  <Box>
    <FormattedMessage id="newsletter.header">
      {txt => <Heading sx={{ fontSize: 5, mb: 4 }}>{txt}</Heading>}
    </FormattedMessage>
    <NewsletterForm />
  </Box>
);
