import { Button, FieldSet, Heading, Input, Text } from "fannypack";
import { graphql, useStaticQuery } from "gatsby";
import React, { useState } from "react";
import { FormattedMessage } from "react-intl";
// @ts-ignore
import { useMailchimp } from "react-use-mailchimp";
import styled from "styled-components";

import { theme } from "../../config/theme";
import { UrlMailchimpQuery } from "../../generated/graphql";
import { Form } from "../form";

export const InputWrapper = styled.div`
  div {
    display: block;
    color: ${theme.palette.text};
    margin-bottom: 0.5rem;
  }
`;

const NewsletterForm: React.SFC = () => {
  const [email, setEmail] = useState("");

  const {
    backend: {
      conference: { urlMailchimp },
    },
  } = useStaticQuery<UrlMailchimpQuery>(query);

  const [mailchimp, subscribe] = useMailchimp({
    url: urlMailchimp,
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
        if (!loading) {
          subscribe({ EMAIL: email });
        }
      }}
    >
      <FieldSet>
        <InputWrapper>
          <Input
            placeholder="my@email.org"
            onChange={(e: any) => setEmail(e.target.value)}
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

const query = graphql`
  query urlMailchimp {
    backend {
      conference {
        urlMailchimp
      }
    }
  }
`;
