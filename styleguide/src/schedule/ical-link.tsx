import React from "react";

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
  return <span title="Download ical">📆</span>;
};
