import clsx from "clsx";
import React from "react";
import { EventWithPerformer, Event } from "./types";

const hasSinglePerformer = (event: Event): event is EventWithPerformer => {
  return (event as EventWithPerformer).performer !== undefined;
};

export const ScheduleItem = ({
  event,

  ...props
}: {
  event: Event;

  style: React.CSSProperties;
}) => {
  const background = {
    LIVE_CODING: "bg-keppel",
    PERFORMANCE: "bg-aquamarine",
    INTERMISSION: "bg-white",
    LIGHTNING_TALK: "bg-casablanca",
    QUIZ: "bg-purple",
    CLOSING: "bg-aquamarine",
    DIVERSITY_SUCCESS_STORY: "bg-orange",
    AMA: "bg-keppel",
  }[event.type];

  return (
    <div
      key={event.start}
      className={clsx("flex flex-col p-4", background)}
      {...props}
    >
      {event.title}
      <footer className="mt-auto">
        {hasSinglePerformer(event) ? event.performer.fullName : null}
      </footer>
    </div>
  );
};
