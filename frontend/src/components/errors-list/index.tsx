/** @jsxImportSource theme-ui */

import { Box, ThemeUIStyleObject } from "theme-ui";

type Props = {
  errors?: string[];
  sx?: ThemeUIStyleObject;
};

export const ErrorsList = ({ errors, ...props }: Props) => {
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
