import clsx from "clsx";
import React from "react";
import { EventWithPerformer, Event, EventWithPerformers } from "./types";

const getPerformers = (event: Event) => {
  const performer = (event as EventWithPerformer).performer || null;

  if (performer) {
    return [performer];
  }

  return (event as EventWithPerformers).performers || [];
};

const getTitle = (event: Event, performers: { fullName: string }[]) => {
  if (event.type === "LIVE_CODING") {
    return `Live coding with ${performers.map((p) => p.fullName).join("&")}`;
  }

  return event.title;
};

export const ScheduleItem = ({
  event,
  className,
  ...props
}: {
  event: Event;
  style: React.CSSProperties;
  className?: string;
}) => {
  const performers = getPerformers(event);

  const background = {
    LIVE_CODING: "bg-keppel",
    PERFORMANCE: "bg-cornflower-blue",
    INTERMISSION: "bg-white",
    LIGHTNING_TALK: "bg-casablanca",
    QUIZ: "bg-purple",
    INTERVIEW: "bg-pink",
    CLOSING: "bg-cornflower-blue",
    DIVERSITY_SUCCESS_STORY: "bg-orange",
    AMA: "bg-keppel",
  }[event.type];

  if (event.status == "TBC") {
    return (
      <div
        key={event.start}
        className={clsx(
          "flex flex-col p-4 font-bold text-white bg-aquamarine",
          className
        )}
        {...props}
      >
        To be announced
      </div>
    );
  }

  return (
    <div
      key={event.start}
      className={clsx("flex flex-col p-4 font-bold justify-between", background, className)}
      {...props}
    >
      <div>
        {getTitle(event, performers)}
      </div>
      <footer className="font-normal text-white">
        {performers.map((p) => p.fullName).join(" & ")}
      </footer>
    </div>
  );
};
