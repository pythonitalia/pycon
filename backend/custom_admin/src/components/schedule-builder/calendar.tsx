import React, { Fragment } from "react";

import { useDjangoAdminEditor } from "../shared/django-admin-editor-modal/context";
import { formatHour } from "../utils/time";
import { Item } from "./item";
import { Placeholder } from "./placeholder";
import type { ConferenceScheduleQuery } from "./schedule.generated";
import { SlotCreation } from "./slot-creation";

type Props = {
  day: ConferenceScheduleQuery["conferenceSchedule"]["days"][0];
};

export const Calendar = ({ day }: Props) => {
  const { id, day: date, rooms, slots } = day;
  const { open } = useDjangoAdminEditor();
  const numOfRooms = rooms.length;
  let rowStartPos = 2;

  const openDayInAdmin = (e) => {
    e.preventDefault();
    const url = `/schedule/day/${id}/change`;
    open(url);
  };

  return (
    <div className="mb-6">
      <span className="sticky top-0 flex items-center gap-3 z-[100] bg-white">
        <h1 className="text-red-900 text-3xl">{date}</h1>
        <a className="underline" href="#" onClick={openDayInAdmin}>
          Edit day in admin
        </a>
      </span>
      <div
        className="grid gap-1"
        style={{
          gridTemplateColumns: `70px repeat(${numOfRooms}, minmax(150px, 1fr))`,
        }}
      >
        <div></div>
        {rooms.map((room) => (
          <div
            className="sticky p-2 font-semibold flex items-center justify-center top-10 bg-white z-[100]"
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
                {formatHour(slot.hour)} [{slot.duration}m] [
                {slot.type.toLowerCase()}]
              </div>

              {rooms.map((room, index) => (
                <Placeholder
                  key={`placeholder-${slot.id}-${index}`}
                  rowStart={rowStart}
                  rowEnd={rowEnd}
                  index={index}
                  slot={slot}
                  room={room}
                  day={day}
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
      <SlotCreation dayId={id} />
    </div>
  );
};
