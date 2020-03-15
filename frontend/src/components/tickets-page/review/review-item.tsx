/** @jsx jsx */
import { Text } from "@theme-ui/components";
import React, { Fragment } from "react";
import { jsx } from "theme-ui";

export const ReviewItem = ({
  label,
  value = "",
}: {
  label: string | React.ReactElement;
  value?: string | React.ReactElement;
}) => (
  <Fragment>
    <Text
      as="span"
      sx={{
        fontWeight: "bold",
      }}
    >
      {label}
    </Text>
    <Text
      sx={{
        wordWrap: "break-word",
      }}
      as="span"
    >
      {value || "-"}
    </Text>
  </Fragment>
);
