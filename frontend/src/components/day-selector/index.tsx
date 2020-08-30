/** @jsx jsx */
import { useRouter } from "next/router";
import React from "react";
import { Box, jsx, Select } from "theme-ui";

import { Link } from "~/components/link";
import { useCurrentLanguage } from "~/locale/context";

import { formatDay } from "./format-day";

// TODO: beginners day could be an attribute on the backend

const getDayUrl = (language: string, day: string) =>
  `/${language}/schedule/${day}`;

export const DaySelector: React.SFC<{
  currentDay: string | null;
  days: {
    day: string;
  }[];
}> = ({ currentDay, days }) => {
  const router = useRouter();
  const language = useCurrentLanguage();

  return (
    <React.Fragment>
      <Box sx={{ display: ["block", "none"] }}>
        <Select
          sx={{ mt: 3, width: "100%" }}
          onChange={(e: React.ChangeEvent<HTMLSelectElement>) =>
            router.push(getDayUrl(language, e.target.value))
          }
        >
          {days.map((day, index) => (
            <option
              key={day.day}
              value={day.day}
              selected={currentDay === day.day}
            >
              {formatDay(day.day, language)} {index === 0 && "(Beginners day)"}
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
            <Link
              path={getDayUrl(language, day.day)}
              variant="button"
              sx={{
                backgroundColor: currentDay === day.day ? "violet" : "white",
                py: 1,
                mr: "-4px",
                position: "relative",
                textTransform: "none",
                "&:hover": {
                  backgroundColor: "lightViolet",
                },
              }}
              after={
                index === 0 && (
                  <Box
                    sx={{
                      color: currentDay === day.day ? "white" : "red",
                      position: "absolute",
                      fontSize: 10,
                      fontWeight: "bold",
                      top: "2px",
                      right: "8px",
                      lineHeight: 1.2,
                    }}
                  >
                    Beginners day
                  </Box>
                )
              }
            >
              {formatDay(day.day, language)}
            </Link>
          </Box>
        ))}
      </Box>
    </React.Fragment>
  );
};
