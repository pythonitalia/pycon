/** @jsx jsx */ import {
  Box,
  Button,
  Heading,
  Input,
  Label,
  Text,
} from "@theme-ui/components";
import { useState } from "react";
import { FormattedMessage } from "react-intl";
import { jsx } from "theme-ui";

const NewsletterForm = () => {
  const [email, setEmail] = useState("");
  const loading = false;
  const error = "";
  const data = undefined;

  const canSubmit = email.trim() !== "" && !loading;

  if (data) {
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
    <Box
      sx={{
        maxWidth: "container",
        mx: "auto",
        px: 2,
      }}
    >
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
