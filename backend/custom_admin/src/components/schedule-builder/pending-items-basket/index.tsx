import clsx from "clsx";
import { useDrop } from "react-dnd";

import { useCurrentConference } from "../../utils/conference";
import { useChangeScheduleItemSlotMutation } from "../change-schedule-item-slot.generated";
import { ScheduleItemCard } from "../item";
import { useUnassignedScheduleItemsQuery } from "./unassigned-schedule-items.generated";

export const PendingItemsBasket = () => {
  const conferenceId = useCurrentConference();
  const { data } = useUnassignedScheduleItemsQuery({
    variables: {
      conferenceId,
    },
  });
  const [changeScheduleItemSlot] = useChangeScheduleItemSlotMutation({
    refetchQueries: ["UnassignedScheduleItems"],
  });

  const [{ isOver, canDrop }, dropRef] = useDrop(
    () => ({
      accept: "scheduleItem",
      drop: async ({ item }) => {
        changeScheduleItemSlot({
          variables: {
            input: {
              conferenceId,
              newSlotId: null,
              rooms: [],
              scheduleItemId: item.id,
            },
          },
        });
      },
      collect: (mon) => ({
        isOver: !!mon.isOver(),
        canDrop: !!mon.canDrop(),
      }),
    }),
    [],
  );

  const items = data?.unassignedScheduleItems ?? [];
  const isEmpty = items.length === 0;

  return (
    <>
      <div className="h-48" />

      <div
        className={clsx(
          "fixed bottom-5 w-full z-[100] flex items-center justify-center transition-transform",
          {
            "translate-y-[110%]": isEmpty && !canDrop,
            "translate-y-0": !isEmpty || canDrop,
          },
        )}
      >
        <div
          ref={dropRef}
          className="relative bg-slate-100 min-h-48 max-w-7xl w-full"
        >
          <div
            className={clsx(
              "absolute top-3 left-3 right-3 bottom-3 flex items-center justify-center border-dotted border-2 border-slate-500 transition-opacity opacity-0 pointer-events-none",
              {
                "opacity-100 pointer-events-auto": canDrop,
              },
            )}
          >
            <span className="font-bold opacity-50 uppercase">
              Drop here to unassign from slot
            </span>
          </div>
          <div
            className={clsx(
              "p-3 transition-opacity flex gap-3 overflow-scroll",
              {
                "opacity-20": canDrop,
              },
            )}
          >
            {items.map((item) => (
              <PendingItemCard key={item.id} item={item} />
            ))}
          </div>
        </div>
      </div>
    </>
  );
};

const PendingItemCard = ({ item }) => {
  return (
    <div className="shrink-0 max-w-80">
      <ScheduleItemCard
        item={item}
        duration={item.duration || item.proposal?.duration}
      />
    </div>
  );
};
