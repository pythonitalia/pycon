/** @jsx jsx */
import { Box, Button } from "@theme-ui/components";
import React from "react";
import { jsx } from "theme-ui";

const formatDay = (day: string) => {
  const d = new Date(day);

  const formatter = new Intl.DateTimeFormat("default", {
    weekday: "long",
    day: "numeric",
    // TODO: use conference timezone
    timeZone: "Europe/Rome",
  });

  return formatter.format(d);
};

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
