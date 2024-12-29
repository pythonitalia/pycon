import { Spacer, Text } from "@python-italia/pycon-styleguide";
import { FormattedMessage } from "react-intl";

import {
  type InvitationLetterRequest,
  InvitationLetterRequestStatus,
} from "~/types";

export const InvitationLetterRequestStatusCallout = ({
  invitationLetterRequest,
}: {
  invitationLetterRequest: InvitationLetterRequest;
}) => (
  <>
    <Spacer size="thin" />
    {invitationLetterRequest.status ===
      InvitationLetterRequestStatus.Pending && (
      <Text size={2}>
        <FormattedMessage id="invitationLetterForm.requestStatus.pending" />
      </Text>
    )}
    {invitationLetterRequest.status === InvitationLetterRequestStatus.Sent && (
      <Text size={2}>
        <FormattedMessage id="invitationLetterForm.requestStatus.sent" />
      </Text>
    )}
    {invitationLetterRequest.status ===
      InvitationLetterRequestStatus.Rejected && (
      <Text size={2}>
        <FormattedMessage id="invitationLetterForm.requestStatus.rejected" />
      </Text>
    )}
  </>
);
