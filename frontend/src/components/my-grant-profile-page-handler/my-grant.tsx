import {
  Button,
  Grid,
  GridColumn,
  Link,
  Spacer,
  Text,
  VerticalStack,
} from "@python-italia/pycon-styleguide";
import { FormattedMessage } from "react-intl";

import { useCurrentLanguage } from "~/locale/context";
import { DeadlineStatus, Status as GrantStatus } from "~/types";
import type { MyProfileWithGrantQuery } from "~/types";

import { createHref } from "../link";
import { GrantTableInfo } from "./grant-table-info";
import { Sidebar } from "./sidebar";

type Props = {
  grant: MyProfileWithGrantQuery["me"]["grant"];
  deadline: MyProfileWithGrantQuery["conference"]["deadline"];
};

const grantManageableStatuses = [
  GrantStatus.WaitingForConfirmation,
  GrantStatus.Confirmed,
  GrantStatus.WaitingList,
  GrantStatus.WaitingListMaybe,
];

export const MyGrant = ({ grant, deadline }: Props) => {
  const language = useCurrentLanguage();

  const canManageGrant = grantManageableStatuses.includes(grant.status);

  const dateFormatter = new Intl.DateTimeFormat(language, {
    day: "numeric",
    month: "long",
    year: "numeric",
  });

  return (
    <>
      <Grid cols={12}>
        <GridColumn colSpan={4}>
          <Sidebar
            status={grant.status}
            grantType={grant.grantType}
            needsFundsForTravel={grant.needsFundsForTravel}
            needAccommodation={grant.needAccommodation}
          />
          {deadline?.status === DeadlineStatus.HappeningNow && (
            <>
              <Spacer size="medium" />
              <Button
                href={createHref({
                  path: "/grants/edit",
                  locale: language,
                })}
                size="small"
                variant="secondary"
              >
                <FormattedMessage id="profile.myGrant.edit" />
              </Button>
            </>
          )}
        </GridColumn>

        <GridColumn colSpan={8}>
          <VerticalStack gap="medium" justifyContent="spaceBetween" fullHeight>
            <div>
              <Text size="label3" uppercase weight="strong">
                <FormattedMessage id="profile.myGrant.nextSteps" />
              </Text>
              <Spacer size="xs" />
              <Text>
                <FormattedMessage
                  id={`profile.myGrant.status.${grant.status}.nextSteps`}
                  values={{
                    replyDeadline: (
                      <Text as="span" weight="strong">
                        {dateFormatter.format(
                          new Date(grant.applicantReplyDeadline),
                        )}
                      </Text>
                    ),
                  }}
                />
              </Text>
            </div>

            {canManageGrant && (
              <div>
                <Button
                  href={createHref({
                    path: "/grants/reply",
                    locale: language,
                  })}
                  size="small"
                  variant="secondary"
                >
                  <FormattedMessage id="profile.myGrant.manage" />
                </Button>
              </div>
            )}

            <GrantTableInfo grant={grant} />

            {deadline?.status === DeadlineStatus.HappeningNow && (
              <Text>
                <FormattedMessage
                  id="profile.myGrant.editInfo"
                  values={{
                    editDeadline: (
                      <Text as="span" weight="strong">
                        {dateFormatter.format(new Date(deadline.end))}
                      </Text>
                    ),
                  }}
                />
              </Text>
            )}

            {canManageGrant && (
              <Text>
                <FormattedMessage id="profile.myGrant.manage.warning" />
              </Text>
            )}
          </VerticalStack>
        </GridColumn>
      </Grid>
    </>
  );
};
