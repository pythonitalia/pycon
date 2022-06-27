/** @jsxRuntime classic */

/** @jsx jsx */
import React from "react";
import { Box, jsx, Select } from "theme-ui";

import { useCurrentLanguage } from "~/locale/context";
import { getDayUrl } from "~/pages/schedule/[day]";

import { formatDay } from "./format-day";

// TODO: beginners day could be an attribute on the backend

export const DaySelector: React.FC<{
  currentDay: string | null;
  timezone: string;
  days: {
    day: string;
  }[];
  changeDay: (day: string) => void;
}> = ({ currentDay, days, timezone, changeDay }) => {
  const language = useCurrentLanguage();

  return (
    <React.Fragment>
      <Box sx={{ display: ["block", "none"] }}>
        <Select
          sx={{ mt: 3, width: "100%" }}
          onChange={(e: React.ChangeEvent<HTMLSelectElement>) =>
            changeDay(e.target.value)
          }
        >
          {days.map((day, index) => (
            <option
              key={day.day}
              value={day.day}
              selected={currentDay === day.day}
            >
              {formatDay(day.day, language, timezone)}{" "}
              {index === 0 && "(Beginners day)"}
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
        {days.map((day) => (
          <Box
            key={day.day}
            as="li"
            sx={{
              listStyle: "none",
              display: "inline-block",
            }}
          >
            <Box
              variant="button"
              as="a"
              // @ts-ignore
              href={getDayUrl(day.day)}
              onClick={(e) => {
                e.preventDefault();
                changeDay(day.day);
              }}
              sx={{
                px: 3,
                fontSize: 2,
                lineHeight: "43px",
                display: "inline-block",
                fontFamily: "body",
                fontWeight: "heading",
                color: "#000",
                textDecoration: "none",
                border: "primary",
                backgroundColor: currentDay === day.day ? "violet" : "white",
                py: 1,
                mr: "-4px",
                position: "relative",
                textTransform: "none",
                userSelect: "none",
                "&:hover": {
                  backgroundColor: "lightViolet",
                },
                cursor: "pointer",
              }}
            >
              {formatDay(day.day, language, timezone)}
            </Box>
          </Box>
        ))}
      </Box>
    </React.Fragment>
  );
};
