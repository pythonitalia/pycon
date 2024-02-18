import {
  Button,
  Container,
  Heading,
  Spacer,
  Text,
} from "@python-italia/pycon-styleguide";
import React from "react";
import { FormattedMessage } from "react-intl";

import { useCurrentLanguage } from "~/locale/context";

import { createHref } from "../link";

type Props = { email: string };
export const NoTickets = ({ email }: Props) => {
  const language = useCurrentLanguage();
  return (
    <Container size="small" center={false} noPadding>
      <Heading size={2}>
        <FormattedMessage id="profile.myTickets.noTickets.heading" />
      </Heading>
      <Spacer size="medium" />
      <Text size={2}>
        <FormattedMessage
          id="profile.myTickets.noTickets.body"
          values={{
            email,
          }}
        />
      </Text>
      <Spacer size="large" />

      <Button
        href={createHref({
          path: "/tickets",
          locale: language,
        })}
      >
        <FormattedMessage id="profile.myTickets.buyTickets" />
      </Button>
    </Container>
  );
};
