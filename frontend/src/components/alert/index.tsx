import { Box } from "@theme-ui/components";
import React from "react";

type Props = {
  variant: "alert" | "success";
};

export const Alert: React.SFC<Props> = ({ variant, children }) => {
  const backgroundColor = variant === "success" ? "green" : "red";
  return (
    <Box
      sx={{
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
    >
      {children}
    </Box>
  );
};
