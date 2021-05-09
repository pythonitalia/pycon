import clsx from "clsx";
import { format } from "date-fns";
import differenceInMinutes from "date-fns/esm/fp/differenceInMinutes/index.js";
import parseISO from "date-fns/parseISO";
import React, { Fragment } from "react";
import { Title } from "../title";

type Props = {
  children: React.ReactNode;
};

export type Performer = {
  fullName: string;
  profilePicture: string;
};

export type Status = "CONFIRMED" | "TBC";

export type BaseEvent = {
  start: string;
  end: string;
  title: string;
  type:
    | "LIVE_CODING"
    | "PERFORMANCE"
    | "INTERMISSION"
    | "LIGHTNING_TALK"
    | "QUIZ"
    | "CLOSING"
    | "ARTISTIC_PERFORMANCE"
    | "DIVERSITY_SUCCESS_STORY"
    | "AMA";
};

export type EventWithPerformer = BaseEvent & {
  status: Status;
  performer: Performer;
};

export type EventWithPerformers = BaseEvent & {
  status: Status;
  performers: Performer[];
};

export type Event = BaseEvent | EventWithPerformer | EventWithPerformers;

export type Day = {
  date: string;
  mc: Performer & {
    status: Status;
  };
  events: Event[];
};
export type Schedule = {
  days: Day[];
};

const SCHEDULE: Schedule = {
  days: [
    {
      date: "2021-06-16",
      mc: {
        fullName: "Harry Percival",
        profilePicture: "...",
        status: "TBC",
      },
      events: [
        {
          start: "2021-06-16T17:00",
          end: "2021-06-16T20:00",
          type: "LIVE_CODING",
          title: "Live Coding with Aaron Bassett",
          performer: {
            fullName: "Aaron Bassett",
            profilePicture: "...",
          },
          status: "TBC",
        },

        {
          start: "2021-06-16T20:00",
          end: "2021-06-16T20:15",
          type: "INTERMISSION",
          title: "Live Coding wrap up",
        },

        {
          start: "2021-06-16T20:15",
          end: "2021-06-16T20:30",
          type: "PERFORMANCE",
          title: "Artistic Performance by Ania Wsz",
          performer: {
            fullName: "Ania Wsz",
            profilePicture: "...",
          },
          status: "CONFIRMED",
        },

        {
          start: "2021-06-16T20:30",
          end: "2021-06-16T20:40",
          type: "LIGHTNING_TALK",
          title: "Lightning talk by Tania Allard",
          performer: {
            fullName: "Tania Allard",
            profilePicture: "...",
          },
          status: "CONFIRMED",
        },

        {
          start: "2021-06-16T20:40",
          end: "2021-06-16T20:50",
          type: "LIGHTNING_TALK",
          title: "Lightning talk by Alessandro Molina",
          performer: {
            fullName: "Alessandro Molina",
            profilePicture: "...",
          },
          status: "CONFIRMED",
        },

        {
          start: "2021-06-16T20:50",
          end: "2021-06-16T21:10",
          type: "DIVERSITY_SUCCESS_STORY",
          title: "Diversity Success Story - TBD",
          performers: [
            {
              fullName: "Fiorella De Luca",
              profilePicture: "...",
            },
            {
              fullName: "Sabrina Scoma",
              profilePicture: "...",
            },
            {
              fullName: "Ambra Tonon",
              profilePicture: "...",
            },
          ],
          status: "TBC",
        },

        {
          start: "2021-06-16T21:10",
          end: "2021-06-16T22:00",
          type: "AMA",
          title: "PSF - Ask Me Anything",
          performers: [
            {
              fullName: "Lelio Campanile",
              profilePicture: "...",
            },
            {
              fullName: "Luca Fedrizzi",
              profilePicture: "...",
            },
          ],
          status: "CONFIRMED",
        },

        {
          start: "2021-06-16T22:00",
          end: "2021-06-16T22:10",
          type: "LIGHTNING_TALK",
          title: "Lightning Talk - TBD",
          performer: {
            fullName: "TBC",
            profilePicture: "...",
          },
          status: "TBC",
        },

        {
          start: "2021-06-16T22:10",
          end: "2021-06-16T22:30",
          type: "ARTISTIC_PERFORMANCE",
          title: "Artistic Performance - TBD",
          performer: {
            fullName: "TBC",
            profilePicture: "...",
          },
          status: "TBC",
        },

        {
          start: "2021-06-16T22:30",
          end: "2021-06-16T23:30",
          type: "QUIZ",
          title: "Pub Quiz",
          status: "CONFIRMED",
        },

        {
          start: "2021-06-16T23:30",
          end: "2021-06-16T23:40",
          type: "CLOSING",
          title: "Closing session",
          status: "CONFIRMED",
        },
      ],
    },
  ],
};

const hasSinglePerformer = (event: Event): event is EventWithPerformer => {
  return (event as EventWithPerformer).performer !== undefined;
};

const ScheduleItem = ({
  event,
  className,
  ...props
}: {
  event: Event;
  className: string;
  style: React.CSSProperties;
}) => {
  return (
    <div
      key={event.start}
      className={clsx("flex flex-col", className)}
      {...props}
    >
      {event.title}
      <footer className="mt-auto">
        {hasSinglePerformer(event) ? event.performer.fullName : null}
      </footer>
    </div>
  );
};

const Day = ({ day, slots }: { day: Day; slots: Slot[] }) => {
  return (
    <Fragment>
      {day.events.map((event, index) => {
        const slot = slots[index];

        return (
          <ScheduleItem
            key={event.start}
            event={event}
            className="bg-white p-4"
            style={{
              gridRowStart: slot.rowStart,
              gridRowEnd: slot.rowEnd,
            }}
          />
        );
      })}
    </Fragment>
  );
};

const getFirstAndLastTime = (events: { start: string; end: string }[]) => {
  const times = events
    .flatMap((e) => [parseISO(e.start), parseISO(e.end)])
    .sort();

  return [times[0], times[times.length - 1]];
};

type Slot = {
  start: Date;
  end: Date;
  rowStart: number;
  rowEnd: number;
};

const TimeSlots = ({ slots }: { slots: Slot[] }) => (
  <Fragment>
    {slots.map((slot) => {
      return (
        <div
          key={slot.start.toString()}
          className="bg-white text-center py-4"
          style={{
            gridRowStart: slot.rowStart,
            gridRowEnd: slot.rowEnd,
          }}
        >
          {format(slot.start, "HH:mm")}
        </div>
      );
    })}
  </Fragment>
);

const getSlots = (events: Event[], uniformSize: boolean = false) => {
  const slots: Slot[] = [];

  events.forEach((event, index) => {
    const start = parseISO(event.start);
    const end = parseISO(event.end);

    const totalMinutes = differenceInMinutes(start, end);
    const rows = uniformSize ? 10 : totalMinutes / 5;

    const rowStart = index === 0 ? 1 : slots[index - 1].rowEnd;
    const rowEnd = rowStart + rows;

    slots.push({
      start,
      end,
      rowStart,
      rowEnd,
    });
  });

  return slots;
};

export const Schedule = ({ children }: Props) => {
  const uniformSize = true;

  const events = SCHEDULE.days[0].events;

  const slots = getSlots(events, uniformSize);
  const [start, end] = getFirstAndLastTime(events);

  const totalMinutes = differenceInMinutes(start, end);
  const rows = uniformSize ? events.length * 10 : totalMinutes / 5;

  return (
    <div>
      <header className="bg-red-500 py-8">
        <div className="max-w-7xl m-auto">
          <Title marginBottom={false}>Schedule June 2021</Title>
        </div>
      </header>

      <div
        className="grid gap-1 bg-black"
        style={{
          gridTemplateRows: `repeat(${rows}, 10px)`,
          gridTemplateColumns: `80px repeat(3, 1fr)`,
        }}
      >
        <TimeSlots slots={slots} />

        <Day day={SCHEDULE.days[0]} slots={slots} />
        <Day day={SCHEDULE.days[0]} slots={slots} />
        <Day day={SCHEDULE.days[0]} slots={slots} />
      </div>
    </div>
  );
};
