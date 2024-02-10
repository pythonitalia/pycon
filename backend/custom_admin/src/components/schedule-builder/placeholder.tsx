import clsx from "clsx";
import { useDrop } from "react-dnd";

import type { Day, Room, ScheduleItem, Slot } from "../../types";
import { useCurrentConference } from "../utils/conference";
import { useAddItemModal } from "./add-item-modal/context";
import { useChangeScheduleItemSlotMutation } from "./change-schedule-item-slot.generated";

type Props = {
  rowStart: number;
  rowEnd: number;
  index: number;
  slot: Slot;
  room: Room;
  day: Day;
};

export const Placeholder = ({
  rowStart,
  rowEnd,
  index,
  slot,
  room,
  day,
}: Props) => {
  const { conferenceId } = useCurrentConference();
  const { open, data } = useAddItemModal();
  const [changeScheduleItemSlot, { loading: isMovingItemLoading }] =
    useChangeScheduleItemSlotMutation({
      refetchQueries: ["UnassignedScheduleItems"],
    });

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

  const openAddModal = () => {
    open({
      day,
      slot,
      room,
    });
  };

  return (
    <div
      ref={dropRef}
      onClick={openAddModal}
      className={clsx(
        "p-2 text-center min-h-48 flex items-center justify-center flex-col cursor-pointer hover:bg-orange-600/50 transition-colors select-none",
        {
          "bg-orange-600/50":
            (isOver && canDrop) ||
            (data?.room?.id === room.id && data?.slot?.id === slot.id),
        },
      )}
      style={{
        gridColumnStart: 2 + index,
        gridColumnEnd: 2 + index,
        gridRowStart: rowStart,
        gridRowEnd: rowEnd,
      }}
    >
      {isMovingItemLoading && <span>Please wait</span>}
      {!isMovingItemLoading && !canDrop && <span>Click to add</span>}
      {!isMovingItemLoading && canDrop && <span>Drop here to move</span>}
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
