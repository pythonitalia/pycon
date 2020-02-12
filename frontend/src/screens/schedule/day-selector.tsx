/** @jsx jsx */
import { Box, Button, Select } from "@theme-ui/components";
import React from "react";
import { jsx } from "theme-ui";

import { formatDay } from "./format-day";

// TODO: beginners day could be an attribute on the backend

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
        {days.map((day, index) => (
          <option
            key={day.day}
            value={day.day}
            selected={currentDay === day.day}
          >
            {formatDay(day.day)} {index === 0 && "(Beginners day)"}
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
      {days.map((day, index) => (
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
              position: "relative",
              "&:hover": {
                backgroundColor: "lightViolet",
              },
            }}
          >
            {formatDay(day.day)}
            {index === 0 && (
              <Box
                sx={{
                  color: "red",
                  position: "absolute",
                  fontSize: 10,
                  fontWeight: "bold",
                  top: "2px",
                  right: "8px",
                }}
              >
                Beginners day
              </Box>
            )}
          </Button>
        </Box>
      ))}
    </Box>
  </React.Fragment>
);
