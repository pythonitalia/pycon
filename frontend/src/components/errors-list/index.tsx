/** @jsxRuntime classic */

/** @jsx jsx */
import { Text } from "@python-italia/pycon-styleguide";
import React from "react";
import { Box, jsx, ThemeUIStyleObject } from "theme-ui";

export const ErrorsList = ({
  errors,
  ...props
}: {
  errors?: (string | React.ReactNode)[];
  sx?: ThemeUIStyleObject;
}) => {
  if (!errors || errors.length === 0) {
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
      {errors.map((error, index) => (
        <Box as="li" key={index} sx={{ pl: 0 }}>
          <Text size="label3" color="red">
            {error}
          </Text>
        </Box>
      ))}
    </Box>
  );
};
