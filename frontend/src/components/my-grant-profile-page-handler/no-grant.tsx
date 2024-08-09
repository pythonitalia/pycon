import {
  Button,
  Container,
  Heading,
  Spacer,
  Text,
} from "@python-italia/pycon-styleguide";
import { FormattedMessage } from "react-intl";

import { useCurrentLanguage } from "~/locale/context";
import { DeadlineStatus, type MyProfileWithSubmissionsQuery } from "~/types";

import { createHref } from "../link";

type Props = {
  deadline: MyProfileWithSubmissionsQuery["conference"]["deadline"];
};

export const NoGrant = ({ deadline }: Props) => {
  const deadlineStatus = deadline.status;
  const language = useCurrentLanguage();

  return (
    <Container size="medium" center={false} noPadding>
      <Heading size={2}>
        <FormattedMessage id="profile.myGrant.noGrant.heading" />
      </Heading>
      <Spacer size="small" />
      <Text size={2}>
        {deadlineStatus === DeadlineStatus.HappeningNow && (
          <FormattedMessage id="profile.myGrant.noGrant.body.canSubmit" />
        )}
        {deadlineStatus === DeadlineStatus.InThePast && (
          <FormattedMessage id="profile.myGrant.noGrant.body.closed" />
        )}
        {deadlineStatus === DeadlineStatus.InTheFuture && (
          <FormattedMessage id="profile.myGrant.noGrant.body.openingSoon" />
        )}
      </Text>
      <Spacer size="large" />
      {deadlineStatus === DeadlineStatus.HappeningNow && (
        <Button
          href={createHref({
            path: "/grants",
            locale: language,
          })}
          variant="secondary"
        >
          <FormattedMessage id="profile.myGrant.noGrant.submitGrant" />
        </Button>
      )}
      {deadlineStatus === DeadlineStatus.InTheFuture && (
        <Button
          href={createHref({
            path: "/grants-info",
            locale: language,
          })}
          variant="secondary"
        >
          <FormattedMessage id="profile.myGrant.noGrant.submitGrant" />
        </Button>
      )}
    </Container>
  );
};
