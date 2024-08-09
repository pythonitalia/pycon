import {
  Button,
  CardPart,
  Grid,
  GridColumn,
  HorizontalStack,
  MultiplePartsCard,
  Spacer,
  Tag,
  Text,
  VerticalStack,
} from "@python-italia/pycon-styleguide";
import { FormattedMessage } from "react-intl";

import { useCurrentLanguage } from "~/locale/context";
import { DeadlineStatus, Status as GrantStatus } from "~/types";
import type { MyProfileWithGrantQuery } from "~/types";

import { Link } from "@python-italia/pycon-styleguide";
import { useCountries } from "~/helpers/use-countries";
import { createHref } from "../link";
import { Sidebar } from "./sidebar";

type Props = {
  grant: MyProfileWithGrantQuery["me"]["grant"];
  deadline: MyProfileWithGrantQuery["conference"]["deadline"];
};

export const MyGrant = ({ grant, deadline }: Props) => {
  const language = useCurrentLanguage();
  const countries = useCountries();

  const canManageGrant = [
    GrantStatus.WaitingForConfirmation,
    GrantStatus.Confirmed,
    GrantStatus.WaitingList,
    GrantStatus.WaitingListMaybe,
  ].includes(grant.status);

  const getCountryLabel = (value: string): string | undefined => {
    const country = countries.find((country) => country.value === value);
    return country ? country.label : undefined;
  };

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
        </GridColumn>

        <GridColumn colSpan={8}>
          <VerticalStack gap="medium" justifyContent="spaceBetween" fullHeight>
            <div>
              <Title>
                <FormattedMessage id="profile.myGrant.nextSteps" />
              </Title>
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

            <Grid cols={3} gap="small" fullWidth>
              <GridColumn>
                <Title>
                  <FormattedMessage id="grants.form.fields.name" />
                </Title>
                <Spacer size="xs" />
                <Text>{grant.name}</Text>
              </GridColumn>

              <GridColumn>
                <Title>
                  <FormattedMessage id="grants.form.fields.fullName" />
                </Title>
                <Spacer size="xs" />
                <Text>{grant.fullName}</Text>
              </GridColumn>

              <GridColumn>
                <Title>
                  <FormattedMessage id="grants.form.fields.ageGroup" />
                </Title>
                <Spacer size="xs" />

                <Text>
                  <FormattedMessage
                    id={`grants.form.fields.ageGroup.values.${grant.ageGroup}`}
                  />
                </Text>
              </GridColumn>

              <GridColumn>
                <Title>
                  <FormattedMessage id="grants.form.fields.travellingFrom" />
                </Title>
                <Spacer size="xs" />
                <Text>{getCountryLabel(grant.travellingFrom)}</Text>
              </GridColumn>

              <GridColumn>
                <Title>
                  <FormattedMessage id="grants.form.fields.gender" />
                </Title>
                <Spacer size="xs" />
                <Text>
                  <FormattedMessage id={`profile.gender.${grant.gender}`} />
                </Text>
              </GridColumn>

              <GridColumn>
                <Title>
                  <FormattedMessage id="grants.form.fields.occupation" />
                </Title>
                <Spacer size="xs" />
                <Text>
                  <FormattedMessage
                    id={`grants.form.fields.occupation.values.${grant.occupation}`}
                  />
                </Text>
              </GridColumn>
            </Grid>
          </VerticalStack>
        </GridColumn>
      </Grid>

      <Spacer size="large" />

      <Grid cols={12} gap="medium">
        <GridColumn colSpan={4}>
          {deadline.status === DeadlineStatus.HappeningNow && (
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
          )}
        </GridColumn>
        <GridColumn colSpan={8}>
          {deadline.status === DeadlineStatus.HappeningNow && (
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
            <>
              <Spacer size="small" />
              <Text>
                <FormattedMessage
                  id="profile.myGrant.manage.warning"
                  values={{
                    grantsEmail: (
                      <Link target="_blank" href="mailto:grants@pycon.it">
                        <Text
                          decoration="underline"
                          weight="strong"
                          color="none"
                        >
                          grants@pycon.it
                        </Text>
                      </Link>
                    ),
                  }}
                />
              </Text>
            </>
          )}
        </GridColumn>
      </Grid>
    </>
  );
};

const Title = ({ children }: { children: React.ReactNode }) => (
  <Text size="label3" uppercase weight="strong">
    {children}
  </Text>
);
