/** @jsx jsx */
import { Box, Text } from "@theme-ui/components";
import React from "react";
import { jsx } from "theme-ui";

export const ReviewItem = ({
  label,
  value,
}: {
  label: string | React.ReactElement;
  value: string | React.ReactElement;
}) => (
  <Box
    as="li"
    sx={{
      mt: 1,
    }}
  >
    <Text
      as="p"
      sx={{
        fontWeight: "bold",
      }}
    >
      {label}
    </Text>
    <Text as="p">{value}</Text>
  </Box>
);
