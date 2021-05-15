import { format } from "date-fns";
import differenceInMinutes from "date-fns/fp/differenceInMinutes";
import parseISO from "date-fns/parseISO";
import React, { Fragment } from "react";
import { Title } from "../title";
import { ScheduleItem } from "./schedule-item";
import { Event, ScheduleProgram, ScheduleDay } from "./types";

type Props = {
  program: ScheduleProgram;
};

const Day = ({ day, slots }: { day: ScheduleDay; slots: Slot[] }) => {
  return (
    <Fragment>
      {day.events.map((event, index) => {
        const slot = slots[index];

        return (
          <ScheduleItem
            key={event.start}
            event={event}
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

const DayHeader = ({ day }: { day: ScheduleDay }) => {
  const date = parseISO(day.date);

  return <div className="bg-white p-4">{format(date, "d MMMM yyyy")}</div>;
};

export const Schedule = ({ program }: Props) => {
  const uniformSize = true;

  const { days } = program;
  const allEvents = days.flatMap((d) => d.events);

  const slots = getSlots(allEvents, uniformSize);
  const [start, end] = getFirstAndLastTime(allEvents);

  const totalMinutes = differenceInMinutes(start, end);
  const rows = uniformSize ? slots.length * 10 : totalMinutes / 5;

  return (
    <div>
      <header className="bg-orange py-8 border-black border-b-4">
        <div className="max-w-7xl m-auto px-8">
          <Title marginBottom={false}>Schedule June 2021</Title>
        </div>
      </header>

      <div
        className="sticky top-0 z-10 grid gap-1 bg-black border-black border-b-4"
        style={{
          gridTemplateColumns: `80px repeat(${days.length}, 1fr)`,
        }}
      >
        <div className="bg-white p-4"></div>

        {days.map((day) => (
          <DayHeader key={day.date} day={day} />
        ))}
      </div>

      <div
        className="grid gap-1 bg-black"
        style={{
          gridTemplateRows: `repeat(${rows}, 10px)`,
          gridTemplateColumns: `80px repeat(${days.length}, 1fr)`,
        }}
      >
        <TimeSlots slots={slots} />

        {days.map((day) => (
          <Day key={day.date} day={day} slots={slots} />
        ))}
      </div>
    </div>
  );
};
