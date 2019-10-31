import { useQuery } from "@apollo/react-hooks";
import * as React from "react";

import { CfpDeadlinesQuery } from "../../generated/graphql-backend";
import { CfpAlert } from "./alert";
import DEADLINES_QUERY from "./deadlines.graphql";

type CfpOpenCheckProps = {
  children: React.ReactNode;
};

export const CfpOpenCheck = (props: CfpOpenCheckProps) => {
  const { loading, error, data } = useQuery<CfpDeadlinesQuery>(DEADLINES_QUERY);

  const isCfpOpen = data && data.conference.isCfpOpen;

  const getMessage = () => {
    const cfpDeadline = data.conference.deadlines.find(
      deadline => deadline.type === "cfp",
    );

    if (!cfpDeadline) {
      return <CfpAlert />;
    }

    let messageId = null;
    let when = null;
    const now = new Date();
    const startDate = new Date(cfpDeadline.start);
    const endDate = new Date(cfpDeadline.end);

    if (now < startDate) {
      messageId = "cfp.from.messages.cfpTooEarly";
      when = startDate;
    }
    if (now > endDate) {
      messageId = "cfp.form.messages.cfpTooLate";
      when = endDate;
    }

    return <CfpAlert messageId={messageId} when={when} />;
  };

  return (
    <>
      {loading && "Loading..."}
      {!loading && isCfpOpen && props.children}
      {!loading && !isCfpOpen && getMessage()}
    </>
  );
};
