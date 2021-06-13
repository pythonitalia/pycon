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

const getSlotKey = ({ start }: { start: string }) =>
  `${format(parseISO(start), "HH:mm")}`;

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
      {day.events.map((event) => {
        const key = getSlotKey(event);
        const slot = slots.find((slot) => slot.key == key);

        if (!slot) {
          console.warn("missing slot for", event);

          return;
        }

        const increase =
          event.size !== undefined ? (event.size - 1) * 10 + 1 : 0;

        return (
          <ScheduleItem
            key={event.start}
            event={event}
            className={className}
            style={{
              gridRowStart: slot.rowStart,
              // TODO: this is a hack to support bigger slots
              gridRowEnd: slot.rowEnd + increase,
            }}
          />
        );
      })}
    </Fragment>
  );
};

type Slot = {
  start: Date;
  end: Date;
  rowStart: number;
  rowEnd: number;
  key: string;
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

    const key = getSlotKey(event);

    if (seenSlots.has(key)) {
      return;
    }

    seenSlots.add(key);

    slots.push({
      start,
      end,
      key,
      rowStart: 0,
      rowEnd: 0,
    });
  });

  slots.sort((a, b) => (a.start < b.start ? -1 : a.start > b.start ? 1 : 0));

  let previousSlot: Slot | null = null;

  for (const slot of slots) {
    const totalMinutes = differenceInMinutes(slot.start, slot.end);
    const rows = uniformSize ? 10 : totalMinutes / 5;

    slot.rowStart = previousSlot?.rowEnd || 1;
    slot.rowEnd = slot.rowStart + rows + 1;

    previousSlot = slot;
  }

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
      className={clsx("p-2 md:p-4 text-center md:text-left", className)}
      onClick={onClick}
    >
      {format(date, "EEEE d MMMM")}
      <span className="hidden md:inline">{format(date, " yyyy")}</span>
    </div>
  );
};

export const Schedule = ({ program }: Props) => {
  const uniformSize = true;

  const days = [program.days[0], program.days[1], program.days[2]];

  const allEvents = days.flatMap((d) => d.events);

  const slots = getSlots(allEvents, uniformSize);
  const rows = Math.max(...slots.map((slot) => slot.rowEnd)) - 1;

  const [selectedDay, setSelectedDay] = useState(days[0].date);

  return (
    <div>
      <header className="bg-orange py-8 border-black border-b-4">
        <div className="max-w-7xl m-auto px-8">
          <Title marginBottom={false}>Schedule</Title>
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
