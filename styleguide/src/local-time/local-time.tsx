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
}) => (
  <time
    dateTime={datetime.toISOString()}
    className="dotted-underline cursor-help"
    title={`This time is using your device's timezone${getUserTimeZone()}.`}
  >
    {format(datetime, FORMAT_MAP[formatType])}
  </time>
);
