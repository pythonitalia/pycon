import React, { Fragment } from "react";

import { formatHour } from "../utils/time";
import { Item } from "./item";
import { Placeholder } from "./placeholder";
import type { ConferenceScheduleQuery } from "./schedule.generated";

type Props = {
  day: ConferenceScheduleQuery["conferenceSchedule"]["days"][0];
};

export const Calendar = ({ day: { day, rooms, slots } }: Props) => {
  const numOfRooms = rooms.length;
  let rowStartPos = 2;

  return (
    <div className="mb-6">
      <h1 className="text-red-900 text-3xl">{day}</h1>
      <div
        className="grid gap-1"
        style={{
          gridTemplateColumns: `50px repeat(${numOfRooms}, minmax(150px, 1fr))`,
        }}
      >
        <div></div>
        {rooms.map((room) => (
          <div
            className="sticky p-2 font-semibold flex items-center justify-center top-0 bg-white z-[100]"
            key={room.id}
          >
            {room.name}
          </div>
        ))}
        {slots.map((slot) => {
          const rowStart = rowStartPos;
          let rowEnd = rowStart + 1;
          rowStartPos = rowEnd;
          return (
            <Fragment key={slot.id}>
              <div
                className="flex items-center font-semibold text-center"
                style={{
                  gridColumnStart: 1,
                  gridColumnEnd: 1,
                  gridRowStart: rowStart,
                  gridRowEnd: rowEnd,
                }}
              >
                {formatHour(slot.hour)} [{slot.duration} mins]
              </div>

              {rooms.map((room, index) => (
                <Placeholder
                  key={`placeholder-${slot.id}-${index}`}
                  rowStart={rowStart}
                  rowEnd={rowEnd}
                  index={index}
                  slot={slot}
                  room={room}
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
