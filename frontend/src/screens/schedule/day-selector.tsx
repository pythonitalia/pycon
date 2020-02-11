/** @jsx jsx */
import { Box, Button } from "@theme-ui/components";
import React from "react";
import { jsx } from "theme-ui";

import { formatDay } from "./format-day";

export const DaySelector: React.SFC<{
  setCurrentDay: (day: string) => void;
  currentDay: string | null;
  days: {
    day: string;
  }[];
}> = ({ currentDay, days, setCurrentDay }) => (
  <Box as="ul" sx={{ ml: "auto" }}>
    {days.map(day => (
      <Box
        key={day.day}
        as="li"
        sx={{
          listStyle: "none",
          display: "inline-block",
        }}
      >
        <Button
          onClick={() => setCurrentDay(day.day)}
          sx={{
            backgroundColor: currentDay === day.day ? "violet" : "white",
            mr: "-3px",
            "&:hover": {
              backgroundColor: "lightViolet",
            },
          }}
        >
          {formatDay(day.day)}
        </Button>
      </Box>
    ))}
  </Box>
);
