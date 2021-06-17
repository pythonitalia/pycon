import clsx from "clsx";
import { parseISO } from "date-fns";
import React from "react";
import { LocalTime } from "../local-time/local-time";
import { ICALLink } from "./ical-link";
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

  const performersList = getPerformers(event);

  const title = getTitle(event, performersList);
  const performers = performersList.map((p) => p.fullName).join(" & ");

  const actualStart = event.actualStart ? parseISO(event.actualStart) : null;

  return (
    <div
      key={event.start}
      className={clsx(
        "flex flex-col p-4 font-bold justify-between",
        background,
        className
      )}
      {...props}
    >
      <div className="flex justify-between">
        <div>
          {event.status === "CANCELLED" ? <span>Cancelled 😢</span> : null}
          <div
            className={clsx({
              "line-through": event.status === "CANCELLED",
            })}
          >
            {title}

            {actualStart ? (
              <div className="text-sm font-normal">
                Starts at{" "}
                <LocalTime format="just-time" datetime={actualStart} />
              </div>
            ) : null}
          </div>
        </div>

        {event.status === "CONFIRMED" ? (
          <ICALLink
            title={title || "Unknown"}
            description={performers}
            start={event.start}
            end={event.end}
          />
        ) : null}
      </div>
      <footer
        className={clsx("font-normal text-white", {
          "line-through": event.status === "CANCELLED",
        })}
      >
        {performers}
      </footer>
    </div>
  );
};
