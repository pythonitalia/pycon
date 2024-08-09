import {
  Button,
  CardPart,
  Grid,
  GridColumn,
  MultiplePartsCard,
  Spacer,
  Tag,
  Text,
  VerticalStack,
} from "@python-italia/pycon-styleguide";
import type React from "react";
import type { GrantType, Status } from "~/types";

import { FormattedMessage } from "react-intl";

type Props = {
  status: Status;
  grantType: GrantType;
  needsFundsForTravel: boolean;
  needAccommodation: boolean;
};

export const Sidebar = ({
  status,
  grantType,
  needsFundsForTravel,
  needAccommodation,
}: Props) => {
  const grantStatusColors = {
    approved: "green",
    confirmed: "green",
    did_not_attend: "red",
    pending: "gray",
    refused: "red",
    rejected: "red",
    waiting_for_confirmation: "yellow",
    waiting_list: "coral",
    waiting_list_maybe: "coral",
  };

  return (
    <>
      <MultiplePartsCard>
        <GrantInfo label={<FormattedMessage id="profile.myGrant.status" />}>
          <Tag color={grantStatusColors[status]}>
            <FormattedMessage id={`profile.myGrant.status.${status}`} />
          </Tag>
        </GrantInfo>

        <GrantInfo label={<FormattedMessage id="profile.myGrant.grantType" />}>
          <FormattedMessage
            id={`grants.form.fields.grantType.values.${grantType}`}
          />
        </GrantInfo>

        <GrantInfo label={<FormattedMessage id="profile.myGrant.appliedFor" />}>
          <VerticalStack gap="small">
            <FormattedMessage id="profile.myGrant.appliedFor.ticket" />

            {needsFundsForTravel && (
              <Text size="label2" weight="strong">
                <FormattedMessage id="profile.myGrant.appliedFor.travel" />
              </Text>
            )}

            {needAccommodation && (
              <Text size="label2" weight="strong">
                <FormattedMessage id="profile.myGrant.appliedFor.accommodation" />
              </Text>
            )}
          </VerticalStack>
        </GrantInfo>
      </MultiplePartsCard>
    </>
  );
};

const GrantInfo = ({
  label,
  children,
}: {
  children: React.ReactNode;
  label?: React.ReactNode;
}) => (
  <CardPart contentAlign="left" background="milk">
    <Text uppercase size="label3" weight="strong">
      {label}
    </Text>
    <Spacer size="xs" />

    <Text size="label2" weight="strong">
      {children}
    </Text>
  </CardPart>
);
