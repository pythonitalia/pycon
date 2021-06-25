import React, { Fragment } from "react";
import { Text, ThemeUIStyleObject } from "theme-ui";

export const ReviewItem = ({
  label,
  value = "",
}: {
  label: string | React.ReactElement;
  value?: string | React.ReactElement;
  sx?: ThemeUIStyleObject;
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
