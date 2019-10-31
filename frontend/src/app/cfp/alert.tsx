import { Alert } from "fannypack";
import * as React from "react";
import { FormattedDate, FormattedMessage } from "react-intl";

type CfpAlertProps = {
  messageId?: string;
  when?: Date;
};

export const CfpAlert = (props: CfpAlertProps) => (
  <Alert type="danger">
    {props.when && (
      <>
        <FormattedMessage id={props.messageId} />
        <FormattedDate
          value={props.when}
          year="numeric"
          month="long"
          day="2-digit"
        />
      </>
    )}
    {!props.when && (
      <FormattedMessage id="cfp.form.messages.cfpClosedGeneric" />
    )}
  </Alert>
);
CfpAlert.defaultProps = {
  messageId: "cfp.from.messages.cfpTooEarly",
  when: "",
};
