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
        pl: 0,
      }}
      {...props}
    >
      {errors.map((error) => (
        <Box as="li" key={error} sx={{ pl: 0 }}>
          {error}
        </Box>
      ))}
    </Box>
  );
};
