import clsx from "clsx";
import { format } from "date-fns";
import differenceInMinutes from "date-fns/fp/differenceInMinutes";
import parseISO from "date-fns/parseISO";
import React, { Fragment, useState } from "react";
import { LocalTime } from "../local-time/local-time";
import { Title } from "../title";
import { ScheduleItem } from "./schedule-item";
import { Event, ScheduleProgram, ScheduleDay } from "./types";

type Props = {
  program: ScheduleProgram;
};

const Day = ({
  day,
  slots,
  className,
}: {
  day: ScheduleDay;
  slots: Slot[];
  className?: string;
}) => {
  return (
    <Fragment>
      {day.events.map((event, index) => {
        const slot = slots[index];

        return (
          <ScheduleItem
            key={event.start}
            event={event}
            className={className}
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
          <LocalTime datetime={slot.start} format="just-time" />
        </div>
      );
    })}
  </Fragment>
);

const getSlots = (events: Event[], uniformSize: boolean = false) => {
  const slots: Slot[] = [];

  const seenSlots = new Set();

  events.forEach((event, index) => {
    const start = parseISO(event.start);
    const end = parseISO(event.end);

    const key = `${format(start, "HH:mm")}-${format(end, "HH:mm")}`;

    if (seenSlots.has(key)) {
      return;
    }

    seenSlots.add(key);

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

const DayHeader = ({
  day,
  className,
  onClick,
}: {
  day: ScheduleDay;
  className?: string;
  onClick?: () => void;
}) => {
  // use the first event as the day date to make sure we use the
  // correct day based on the user time zone
  const date = parseISO(day.events[0].start);

  return (
    <div
      className={clsx(
        "p-2 md:p-4 text-center md:text-left",
        className
      )}
      onClick={onClick}
    >
      {format(date, "d MMMM")}
      <span className="hidden md:inline">{format(date, " yyyy")}</span>
    </div>
  );
};

export const Schedule = ({ program }: Props) => {
  const uniformSize = true;

  const days = [program.days[0], program.days[1], program.days[2]];

  const allEvents = days.flatMap((d) => d.events);

  const slots = getSlots(allEvents, uniformSize);
  const [start, end] = getFirstAndLastTime(allEvents);

  const totalMinutes = differenceInMinutes(start, end);
  const rows = uniformSize ? slots.length * 10 : totalMinutes / 5;

  const [selectedDay, setSelectedDay] = useState(days[0].date);

  return (
    <div>
      <header className="bg-orange py-8 border-black border-b-4">
        <div className="max-w-7xl m-auto px-8">
          <Title marginBottom={false}>Schedule June 2021</Title>
        </div>
      </header>

      <div
        className="schedule-head sticky top-0 z-10"
        style={
          {
            "--days": days.length,
          } as any
        }
      >
        <div className="bg-white p-4 hidden md:flex"></div>

        {days.map((day) => (
          <DayHeader
            key={day.date}
            day={day}
            onClick={() => setSelectedDay(day.date)}
            className={clsx(
              {
                "bg-white": day.date !== selectedDay,
                "bg-purple": day.date === selectedDay,
              },
              "md:bg-white"
            )}
          />
        ))}
      </div>

      <div
        className="schedule-head schedule-head-mc"
        style={
          {
            "--days": days.length,
          } as any
        }
      >
        <div className="bg-white p-4 hidden md:flex"></div>

        {days.map((day) => (
          <div
            className={clsx(
              "bg-pink p-2 md:p-4 text-center md:text-left",
              {
                hidden: day.date !== selectedDay,
              },
              "md:block"
            )}
          >
            🎤 MC: <strong className="font-bold">{day.mc.fullName}</strong>
          </div>
        ))}
      </div>

      <div
        className="schedule-grid"
        style={
          {
            "--rows": rows,
            "--days": days.length,
          } as any
        }
      >
        <TimeSlots slots={slots} />

        {days.map((day) => (
          <Day
            key={day.date}
            day={day}
            slots={slots}
            className={clsx(
              {
                hidden: day.date !== selectedDay,
              },
              "md:flex"
            )}
          />
        ))}
      </div>
    </div>
  );
};
