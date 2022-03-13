/** @jsxRuntime classic */

/** @jsx jsx */
import React, { Fragment } from "react";
import { FormattedMessage } from "react-intl";
import { Box, jsx } from "theme-ui";

import { Marquee } from "../marquee";

type Props = {
  goBack: () => void;
  backTo: "schedule" | "keynotes";
};

export const BackToMarquee = ({ goBack, backTo }: Props) => {
  const messageId =
    backTo === "schedule"
      ? "schedule.backToSchedule"
      : "keynote.backToKeynotes";
  return (
    <Fragment>
      <Box
        sx={{
          pt: 4,
        }}
      />
      <Box
        sx={{
          color: "black",
          cursor: "pointer",
        }}
        onClick={goBack}
      >
        <FormattedMessage id={messageId}>
          {(message) => <Marquee separator=">" message={message.join("")} />}
        </FormattedMessage>
      </Box>
    </Fragment>
  );
};
