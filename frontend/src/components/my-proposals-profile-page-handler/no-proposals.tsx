import {
  Button,
  Container,
  Heading,
  Spacer,
  Text,
} from "@python-italia/pycon-styleguide";
import { FormattedMessage } from "react-intl";

import { useCurrentLanguage } from "~/locale/context";
import { DeadlineStatus, MyProfileWithSubmissionsQuery } from "~/types";

import { createHref } from "../link";

type Props = {
  deadline: MyProfileWithSubmissionsQuery["conference"]["deadline"];
};
export const NoProposals = ({ deadline }: Props) => {
  const deadlineStatus = deadline.status;
  const language = useCurrentLanguage();
  return (
    <Container size="small" center={false} noPadding>
      <Heading size={2}>
        <FormattedMessage id="profile.myProposals.noProposals.heading" />
      </Heading>
      <Spacer size="small" />
      <Text size={2}>
        {deadlineStatus === DeadlineStatus.HappeningNow && (
          <FormattedMessage id="profile.myProposals.noProposals.body.canSubmit" />
        )}
        {deadlineStatus === DeadlineStatus.InThePast && (
          <FormattedMessage id="profile.myProposals.noProposals.body.closed" />
        )}
        {deadlineStatus === DeadlineStatus.InTheFuture && (
          <FormattedMessage id="profile.myProposals.noProposals.body.openingSoon" />
        )}
      </Text>
      <Spacer size="large" />
      {(deadlineStatus === DeadlineStatus.HappeningNow ||
        deadlineStatus === DeadlineStatus.InTheFuture) && (
        <Button
          href={createHref({
            path: "/call-for-proposals",
            locale: language,
          })}
          variant="secondary"
        >
          <FormattedMessage id="profile.myProposals.noProposals.submitProposal" />
        </Button>
      )}
      {deadlineStatus === DeadlineStatus.InThePast && (
        <Button
          href={createHref({
            path: "/tickets",
            locale: language,
          })}
          variant="secondary"
        >
          <FormattedMessage id="profile.myTickets.buyTickets" />
        </Button>
      )}
    </Container>
  );
};
