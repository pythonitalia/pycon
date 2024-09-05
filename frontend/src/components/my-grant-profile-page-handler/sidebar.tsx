import {
  CardPart,
  MultiplePartsCard,
  Spacer,
  Tag,
  Text,
  VerticalStack,
} from "@python-italia/pycon-styleguide";
import type { Color } from "@python-italia/pycon-styleguide/dist/types";
import type React from "react";
import { Status as GrantStatus, type GrantType } from "~/types";

import { FormattedMessage } from "react-intl";

type Props = {
  status: GrantStatus;
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
  return (
    <MultiplePartsCard>
      <GrantInfo label={<FormattedMessage id="profile.myGrant.status" />}>
        <Tag color={getStatusColor(status)}>
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

const getStatusColor = (status: GrantStatus): Color => {
  switch (status) {
    case GrantStatus.Approved:
    case GrantStatus.Confirmed:
      return "green";
    case GrantStatus.Pending:
      return "grey";
    case GrantStatus.Refused:
    case GrantStatus.Rejected:
    case GrantStatus.DidNotAttend:
      return "red";
    case GrantStatus.WaitingForConfirmation:
      return "yellow";
    case GrantStatus.WaitingList:
    case GrantStatus.WaitingListMaybe:
      return "coral";
  }
};
