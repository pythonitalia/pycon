import React, { useState } from "react";
import { FieldSet, Heading, Input, Text, Button } from "fannypack";
import { useMailchimp } from "react-use-mailchimp";
import { FormattedMessage } from "react-intl";
import { Form } from "../form";

const url = process.env.MAILCHIMP_URL || "";
console.log(url);
import { theme } from "../../config/theme";
import styled from "styled-components";

export const InputWrapper = styled.div`
  div {
    display: block;
    color: ${theme.palette.text};
    margin-bottom: 0.5rem;
  }
`;

const NewsletterForm: React.SFC = () => {
  const [email, setEmail] = useState("");
  const [mailchimp, subscribe] = useMailchimp({
    url,
  });
  const { loading, error, data } = mailchimp;

  const canSubmit = email.trim() !== "" && !loading;

  if (data && data.result === "success") {
    return (
      <FormattedMessage id="newsletter.success">
        {txt => <Text>{txt}</Text>}
      </FormattedMessage>
    );
  }
  if (error) {
    console.log(error);
    return (
      <FieldSet>
        <Text
          color="danger"
          use="strong"
          dangerouslySetInnerHTML={{ __html: error }}
        />
      </FieldSet>
    );
  }

  return (
    <Form
      onSubmit={e => {
        e.preventDefault();
        console.log(`onSubmit: ${email}`);
        if (!loading) {
          subscribe({ EMAIL: email });
        }
      }}
    >
      <FieldSet>
        <InputWrapper>
          <Input
            placeholder="my@email.org"
            onChange={e => setEmail(e.target.value)}
            value={email}
            isRequired={true}
            type="email"
          />
        </InputWrapper>
        <Button type="submit" disabled={!canSubmit} isLoading={loading}>
          <FormattedMessage id="newsletter.button" />
        </Button>
      </FieldSet>
    </Form>
  );
};

export const NewsletterSection: React.SFC = props => (
  <>
    <FormattedMessage id="newsletter.header">
      {txt => <Heading use="h3">{txt}</Heading>}
    </FormattedMessage>
    <FormattedMessage id="newsletter.text">
      {txt => <Text>{txt}</Text>}
    </FormattedMessage>
    <NewsletterForm />
  </>
);
