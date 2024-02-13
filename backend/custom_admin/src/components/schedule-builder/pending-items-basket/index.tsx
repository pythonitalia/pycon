import clsx from "clsx";
import { useEffect, useRef, useState } from "react";
import { useDrop } from "react-dnd";

import { useCurrentConference } from "../../utils/conference";
import { useChangeScheduleItemSlotMutation } from "../change-schedule-item-slot.generated";
import { ScheduleItemCard } from "../item";
import { useUnassignedScheduleItemsQuery } from "./unassigned-schedule-items.generated";

export const PendingItemsBasket = () => {
  const { conferenceId } = useCurrentConference();
  const { data } = useUnassignedScheduleItemsQuery({
    variables: {
      conferenceId,
    },
  });
  const [changeScheduleItemSlot] = useChangeScheduleItemSlotMutation({
    refetchQueries: ["UnassignedScheduleItems"],
  });
  const itemsRef = useRef<HTMLDivElement>(null);

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
          "fixed bottom-5 w-full z-[100] flex items-center justify-center transition-transform ",
          {
            "translate-y-[110%]": isEmpty && !canDrop,
            "translate-y-0": !isEmpty || canDrop,
          },
        )}
      >
        <div
          ref={dropRef}
          className="relative bg-slate-100 min-h-48 max-w-7xl w-full border-2 border-slate-400"
        >
          <ScrollButton
            direction="backwards"
            scrollElement={itemsRef}
            items={items}
          />

          <div
            className={clsx(
              "absolute top-3 left-3 right-3 bottom-3 flex items-center justify-center border-dotted border-2 border-slate-500 transition-opacity opacity-0 pointer-events-none",
              {
                "opacity-100 pointer-events-auto": canDrop,
              },
            )}
          >
            <span className="font-bold opacity-50 uppercase select-none">
              Drop here to unassign from slot
            </span>
          </div>
          <div
            ref={itemsRef}
            className={clsx(
              "px-12 py-3 transition-opacity flex gap-3 overflow-scroll",
              {
                "opacity-20": canDrop,
              },
            )}
          >
            {items.map((item) => (
              <PendingItemCard key={item.id} item={item} />
            ))}
          </div>

          <ScrollButton
            direction="forwards"
            scrollElement={itemsRef}
            items={items}
          />
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
        duration={item.duration || item.proposal?.duration?.duration}
      />
    </div>
  );
};

const ScrollButton = ({
  direction,
  scrollElement,
  items,
}: {
  direction: "backwards" | "forwards";
  scrollElement: React.RefObject<HTMLDivElement>;
  items: any[];
}) => {
  const [canScroll, setCanScroll] = useState(false);
  const checkCanScroll = () => {
    const element = scrollElement.current;

    if (direction === "forwards") {
      setCanScroll(
        Math.ceil(element.scrollWidth) >
          Math.ceil(element.clientWidth) + Math.ceil(element.scrollLeft),
      );
    } else {
      setCanScroll(element.scrollLeft > 0);
    }
  };
  const scroll = (e) => {
    e.preventDefault();
    if (direction === "forwards") {
      scrollElement.current.scrollBy({
        left: 500,
        behavior: "smooth",
      });
    } else {
      scrollElement.current.scrollBy({
        left: -500,
        behavior: "smooth",
      });
    }
  };

  useEffect(() => {
    if (!scrollElement.current) {
      return;
    }

    checkCanScroll();
    scrollElement.current.addEventListener("scroll", checkCanScroll, {
      passive: true,
    });

    return () => {
      scrollElement.current.removeEventListener("scroll", checkCanScroll);
    };
  }, [scrollElement.current]);

  useEffect(() => {
    checkCanScroll();
  }, [items]);

  if (!canScroll) {
    return null;
  }

  return (
    <div
      onClick={scroll}
      className={clsx(
        "absolute shadow-md p-6 cursor-pointer top-1/2 bg-white rounded-full select-none",
        {
          "-translate-y-1/2 -translate-x-1/2 left-0": direction === "backwards",
          "-translate-y-1/2 translate-x-1/2 right-0": direction === "forwards",
        },
      )}
    >
      {direction === "backwards" ? `👈` : `👉`}
    </div>
  );
};
