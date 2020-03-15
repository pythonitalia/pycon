/** @jsx jsx */
import { Box } from "@theme-ui/components";
import React from "react";
import { jsx } from "theme-ui";

export const ErrorsList: React.SFC<{ errors?: string[] }> = ({
  errors,
  ...props
}) => {
  if (!errors) {
    return null;
  }

  return (
    <Box
      as="ul"
      sx={{
        listStyle: "none",
        color: "red",
      }}
      {...props}
    >
      {errors.map((error) => (
        <Box as="li" key={error}>
          {error}
        </Box>
      ))}
    </Box>
  );
};
