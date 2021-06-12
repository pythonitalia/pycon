import React from "react";
import { format } from "date-fns";

const getUserTimeZone = () => {
  try {
    return ` (${Intl.DateTimeFormat().resolvedOptions().timeZone})`;
  } catch {
    return "";
  }
};

const FORMAT_MAP = {
  full: "d MMMM yyyy 'at' HH:mm",
  "just-time": "HH:mm",
};

export const LocalTime = ({
  datetime,
  format: formatType,
}: {
  datetime: Date;
  format: keyof typeof FORMAT_MAP;
}) => {
  const userTimeZone = getUserTimeZone();

  return (
    <time
      dateTime={datetime.toISOString()}
      className="dotted-underline cursor-help inline-block leading-5"
      title={
        userTimeZone
          ? `This time is using your device's timezone ${userTimeZone}.`
          : ""
      }
    >
      {format(datetime, FORMAT_MAP[formatType])}{" "}
      <span className="text-2xs">({format(datetime, "O")})</span>
    </time>
  );
};
