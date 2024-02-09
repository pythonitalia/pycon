import clsx from "clsx";
import { useDrag, useDrop } from "react-dnd";

import type { Room, ScheduleItem, Slot } from "../../types";
import { useCurrentConference } from "../utils/conference";
import { useChangeScheduleItemSlotMutation } from "./change-schedule-item-slot.generated";

type Props = {
  rowStart: number;
  rowEnd: number;
  index: number;
  slot: Slot;
  room: Room;
};

export const Placeholder = ({ rowStart, rowEnd, index, slot, room }: Props) => {
  const conferenceId = useCurrentConference();
  const [changeScheduleItemSlot, { loading: movingItem }] =
    useChangeScheduleItemSlotMutation({});

  const onMoveItem = async (item: ScheduleItem) => {
    await changeScheduleItemSlot({
      variables: {
        input: {
          conferenceId,
          rooms: [room.id],
          scheduleItemId: item.id,
          newSlotId: slot.id,
        },
      },
    });
  };

  const [{ isOver, canDrop }, dropRef] = useDrop(
    () => ({
      accept: "scheduleItem",
      drop: async ({ item }) => {
        onMoveItem(item);
      },
      collect: (mon) => ({
        isOver: !!mon.isOver(),
        canDrop: !!mon.canDrop(),
      }),
    }),
    [],
  );
  console.log("isOver", isOver);
  return (
    <div
      ref={dropRef}
      className={clsx(
        "p-2 text-center flex items-center justify-center flex-col cursor-pointer hover:bg-orange-600/50 transition-colors",
        {
          "bg-orange-600/50": isOver && canDrop,
        },
      )}
      style={{
        gridColumnStart: 2 + index,
        gridColumnEnd: 2 + index,
        gridRowStart: rowStart,
        gridRowEnd: rowEnd,
      }}
    >
      {movingItem && <span>Please wait</span>}
      Add proposal
      <PlusIcon />
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
