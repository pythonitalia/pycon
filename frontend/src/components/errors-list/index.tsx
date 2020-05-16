/** @jsx jsx */
import React from "react";
import { Box, jsx } from "theme-ui";

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
