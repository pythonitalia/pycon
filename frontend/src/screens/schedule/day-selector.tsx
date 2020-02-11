/** @jsx jsx */
import { Box, Button, Select } from "@theme-ui/components";
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
  <React.Fragment>
    <Box sx={{ display: ["block", "none"] }}>
      <Select
        sx={{ mt: 3, width: "100%" }}
        onChange={(e: React.ChangeEvent<HTMLSelectElement>) =>
          setCurrentDay(e.target.value)
        }
      >
        {days.map(day => (
          <option
            key={day.day}
            value={day.day}
            selected={currentDay === day.day}
          >
            {formatDay(day.day)}
          </option>
        ))}
      </Select>
    </Box>

    <Box
      as="ul"
      sx={{
        mt: [3, null, 0],
        display: ["none", "block"],
      }}
    >
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
  </React.Fragment>
);
