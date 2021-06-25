import React from "react";
import { Box, ThemeUIStyleObject } from "theme-ui";

type Props = {
  variant: "alert" | "success" | "info";
  children: React.ReactNode;
  sx?: ThemeUIStyleObject;
};

export const Alert = ({ variant, children, ...props }: Props) => {
  let backgroundColor;

  switch (variant) {
    case "alert":
      backgroundColor = "red";
      break;
    case "success":
      backgroundColor = "green";
      break;
    case "info":
      backgroundColor = "blue";
      break;
  }

  return (
    <Box
      sx={{
        display: "block",
        my: 2,
      }}
    >
      <Box
        sx={{
          display: "inline-block",

          position: "relative",

          width: "auto",
          py: 4,
          px: 3,
          border: "primary",

          "::before": {
            content: "''",
            display: "block",

            position: "absolute",
            top: 0,
            left: 0,

            width: 10,
            height: "100%",

            backgroundColor,
          },
        }}
        {...props}
      >
        {children}
      </Box>
    </Box>
  );
};
