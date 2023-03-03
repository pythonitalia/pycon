import {
  Button,
  Container,
  Heading,
  Spacer,
  Text,
} from "@python-italia/pycon-styleguide";
import { FormattedMessage } from "react-intl";

import { useCurrentLanguage } from "~/locale/context";

import { createHref } from "../link";

export const NoOrders = () => {
  const language = useCurrentLanguage();
  return (
    <Container size="small" center={false} noPadding>
      <Heading size={2}>
        <FormattedMessage id="profile.myProposals.noOrders.heading" />
      </Heading>
      <Spacer size="small" />
      <Text size={2}>
        <FormattedMessage id="profile.myProposals.noOrders.body" />
      </Text>
      <Spacer size="large" />
      <Button
        role="secondary"
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
