import React from "react";
import ICalendarLink from "react-icalendar-link";

export const ICALLink = ({
  title,
  description,
  start,
  end,
}: {
  title: string;
  description: string;
  start: string;
  end: string;
}) => {
  const event = {
    title,
    description,
    startTime: start,
    endTime: end,
    location: "https://pyfest.online",
    attendees: ["Hello World <hello@world.com>", "Hey <hey@test.com>"],
  };

  return (
    <ICalendarLink event={event}>
      <span title="Download ical">📆</span>
    </ICalendarLink>
  );
};
