import { Alert } from "fannypack";
import * as React from "react";
import { FormattedMessage } from "react-intl";

type CfpAlertProps = {
  messageId?: string;
  when?: string;
};

export const CfpAlert = (props: CfpAlertProps) => (
  <Alert type="danger">
    <FormattedMessage id={props.messageId}>
      {message => message + props.when}
    </FormattedMessage>
  </Alert>
);
CfpAlert.defaultProps = {
  messageId: "cfp.from.messages.cfpTooEarly",
  when: "",
};
