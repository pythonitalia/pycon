import clsx from "clsx";
import { Fragment, useState } from "react";
import { useDrag, useDrop } from "react-dnd";

import { ItemCard } from "./item-card";
import { RoomFragment, ScheduleItemFragment } from "./schedule-item.generated";
import { ScheduleSlotFragment } from "./schedule-slot.generated";
import { ScheduleQuery } from "./schedule.generated";
import { SubmissionFragment } from "./submission.generated";
import { useUpdateSlotMutation } from "./update-slot.generated";

const convertHoursToMinutes = (value: string) => {
  const [hour, minutes] = value.split(":").map((x) => parseInt(x, 10));

  return hour * 60 + minutes;
};

const formatHour = (value: string) => {
  const [hour, minutes] = value.split(":");

  return [hour, minutes].join(".");
};

export const DayScheduleView = ({
  day,
}: {
  day: ScheduleQuery["conference"]["days"][0];
}) => {
  const slots = day.slots;
  const rooms = day.rooms;
  const totalRooms = rooms.length;
  let rowStartPos = 2;

  return (
    <div
      className="grid"
      style={{
        gridTemplateColumns: `50px repeat(${totalRooms}, 1fr)`,
        gap: "0.3rem",
      }}
    >
      <div></div>
      {rooms.map((room) => (
        <div key={room.id} className="sticky top-[52px] bg-white z-[100]">
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
              key={slot.hour}
              style={{
                gridColumnStart: 1,
                gridColumnEnd: 1,
                gridRowStart: rowStart,
                gridRowEnd: rowEnd,
              }}
            >
              {formatHour(slot.hour)}
            </div>

            {rooms.map((room, index) => {
              return (
                <Placeholder
                  key={`${room.id}-${index}`}
                  room={room}
                  rowStart={rowStart}
                  rowEnd={rowEnd}
                  index={index}
                  slot={slot}
                />
              );
            })}

            {slot.items.map((item) => (
              <Item
                key={item.id}
                item={item}
                rooms={rooms}
                slot={slot}
                slots={slots}
                rowStart={rowStart}
              />
            ))}
          </Fragment>
        );
      })}
    </div>
  );
};

const Item = ({
  item,
  rooms,
  slot,
  slots,
  rowStart,
}: {
  item: ScheduleItemFragment;
  rooms: ScheduleQuery["conference"]["days"][0]["rooms"];
  slot: ScheduleSlotFragment;
  slots: ScheduleSlotFragment[];
  rowStart: number;
}) => {
  const [{ opacity }, dragRef] = useDrag(
    () => ({
      type: "item",
      item: {
        ...item,
      },
      collect: (monitor) => ({
        opacity: monitor.isDragging() ? 0.5 : 1,
      }),
    }),
    [],
  );

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
    <ItemCard
      ref={dragRef}
      item={item}
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
    />
  );
};

const Placeholder = ({
  index,
  rowStart,
  rowEnd,
  slot,
  room,
}: {
  room: ScheduleQuery["conference"]["days"][0]["rooms"][0];
  index: number;
  rowStart: number;
  rowEnd: number;
  slot: ScheduleSlotFragment;
}) => {
  const [updateSlot] = useUpdateSlotMutation({
    refetchQueries: ["UnassignedScheduleItems"],
  });
  const [{ isOver, canDrop }, drop] = useDrop(
    () => ({
      accept: "item",
      drop: async (item: ScheduleItemFragment) => {
        console.log("drop", slot, "item", item, "room", room);
        const result = await updateSlot({
          variables: {
            input: {
              slotId: slot.id,
              rooms: [room.id],
              title: "",
              itemId: item.id,
              keynoteId: item.keynote?.id,
              submissionId: item.submission?.id,
            },
          },
        });
        console.log("result", result);
      },
      collect: (mon) => ({
        isOver: !!mon.isOver(),
        canDrop: !!mon.canDrop(),
      }),
    }),
    [],
  );
  console.log("isOver", isOver);
  const [showAddTalkModal, setShowAddTalkModal] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");

  return (
    <>
      <div
        ref={drop}
        style={{
          gridColumnStart: 2 + index,
          gridColumnEnd: 2 + index,
          gridRowStart: rowStart,
          gridRowEnd: rowEnd,
        }}
        className={clsx("relative min-h-[150px] transition-colors", {
          "bg-slate-400": isOver,
        })}
      >
        <div
          onClick={(e) => setShowAddTalkModal(true)}
          className="absolute top-0 left-0 w-full h-full flex flex-col items-center justify-center cursor-pointer transition-colors hover:bg-orange-600/50"
        >
          Add talk
          <PlusIcon />
        </div>
      </div>
      {showAddTalkModal && (
        <div className="fixed inset-0 flex items-center justify-center z-[300]">
          <div
            onClick={(_) => setShowAddTalkModal(false)}
            className="fixed inset-0 w-screen h-screen z-[300] bg-black/80"
          ></div>
          <div className="bg-white p-6 w-full max-w-[600px] z-[400]">
            <p>
              You are adding a proposal to slot {slot.hour} in room {room.name}
            </p>
            <input
              placeholder="Search..."
              className="border border-black w-full"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </div>
        </div>
      )}
    </>
  );
};

const PlusIcon = () => {
  return (
    <svg width="28" height="28" viewBox="0 0 100 100">
      <path d="m50 87.375c20.609 0 37.379-16.766 37.379-37.375s-16.77-37.375-37.379-37.375-37.379 16.766-37.379 37.375 16.77 37.375 37.379 37.375zm-11.707-40.375h8.707v-8.707c0-1.6562 1.3438-3 3-3s3 1.3438 3 3v8.707h8.707c1.6562 0 3 1.3438 3 3s-1.3438 3-3 3h-8.707v8.707c0 1.6562-1.3438 3-3 3s-3-1.3438-3-3v-8.707h-8.707c-1.6562 0-3-1.3438-3-3s1.3438-3 3-3z" />
    </svg>
  );
};
