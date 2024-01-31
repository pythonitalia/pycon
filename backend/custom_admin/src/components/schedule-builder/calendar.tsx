import React, { Fragment } from "react";

import type { ConferenceScheduleQuery } from "./schedule.generated";

type Props = {
  day: ConferenceScheduleQuery["conferenceSchedule"]["days"][0];
};

const convertHoursToMinutes = (value: string) => {
  const [hour, minutes] = value.split(":").map((x) => parseInt(x, 10));

  return hour * 60 + minutes;
};

const formatHour = (value: string) => {
  const [hour, minutes] = value.split(":");

  return [hour, minutes].join(".");
};

export const Calendar = ({ day: { day, rooms, slots } }: Props) => {
  const numOfRooms = rooms.length;
  let rowStartPos = 2;

  return (
    <div>
      <h1 className="text-red-900 text-3xl">{day}</h1>
      <div
        className="grid"
        style={{
          gridTemplateColumns: `100px repeat(${numOfRooms}, 1fr)`,
        }}
      >
        <div></div>
        {rooms.map((room) => (
          <div key={room.id}>{room.name}</div>
        ))}
        {slots.map((slot) => {
          const rowStart = rowStartPos;
          let rowEnd = rowStart + 1;
          rowStartPos = rowEnd;
          return (
            <Fragment key={slot.id}>
              <div
                style={{
                  gridColumnStart: 1,
                  gridColumnEnd: 1,
                  gridRowStart: rowStart,
                  gridRowEnd: rowEnd,
                }}
              >
                {slot.hour}
              </div>

              {rooms.map((room, index) => (
                <Placeholder
                  rowStart={rowStart}
                  rowEnd={rowEnd}
                  index={index}
                />
              ))}

              {slot.items.map((item, index) => (
                <Item
                  key={`item-${item.id}-${index}`}
                  slots={slots}
                  slot={slot}
                  item={item}
                  rooms={rooms}
                  rowStart={rowStart}
                />
              ))}
            </Fragment>
          );
        })}
      </div>
    </div>
  );
};

const Placeholder = ({ rowStart, rowEnd, index }) => {
  return (
    <div
      style={{
        gridColumnStart: 2 + index,
        gridColumnEnd: 2 + index,
        gridRowStart: rowStart,
        gridRowEnd: rowEnd,
      }}
    >
      Add proposal
      <PlusIcon />
    </div>
  );
};

const Item = ({ slots, slot, item, rooms, rowStart }) => {
  const roomIndexes = item.rooms
    .map((room) => rooms.findIndex((r) => r.id === room.id))
    .sort();

  const start = convertHoursToMinutes(slot.hour);
  const duration =
    item.duration || slot.duration || item.submission?.duration?.duration;

  const end = start + duration;

  const currentSlotIndex = slots.findIndex((s) => s.id === slot.id);

  let endingSlotIndex = slots.findIndex(
    (s) => convertHoursToMinutes(s.hour) + s.duration > end,
  );

  if (endingSlotIndex === -1) {
    endingSlotIndex = slots.length;
  }

  const index = roomIndexes[0];
  return (
    <div
      style={{
        gridColumnStart: index + 2,
        gridColumnEnd: index + 2 + item.rooms.length,
        gridRowStart: rowStart,
        gridRowEnd:
          rowStart +
          slots
            .slice(currentSlotIndex, endingSlotIndex)
            .reduce((acc, s) => acc + 1, 0),
      }}
      className="bg-slate-200 p-3 z-50"
    >
      {item.title}
    </div>
  );
};

const PlusIcon = () => {
  return (
    <svg width="28" height="28" viewBox="0 0 100 100">
      <path d="m50 87.375c20.609 0 37.379-16.766 37.379-37.375s-16.77-37.375-37.379-37.375-37.379 16.766-37.379 37.375 16.77 37.375 37.379 37.375zm-11.707-40.375h8.707v-8.707c0-1.6562 1.3438-3 3-3s3 1.3438 3 3v8.707h8.707c1.6562 0 3 1.3438 3 3s-1.3438 3-3 3h-8.707v8.707c0 1.6562-1.3438 3-3 3s-3-1.3438-3-3v-8.707h-8.707c-1.6562 0-3-1.3438-3-3s1.3438-3 3-3z" />
    </svg>
  );
};
