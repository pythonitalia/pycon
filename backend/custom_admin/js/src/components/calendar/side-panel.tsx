import { useDrag, useDrop } from "react-dnd";

import { ItemCard } from "./item-card";
import { useMoveItemMutation } from "./move-item.generated";
import { ScheduleItemFragment } from "./schedule-item.generated";
import { useUnassignedScheduleItemsQuery } from "./unassigned-schedule-items.generated";
import { useUpdateSlotMutation } from "./update-slot.generated";

export const SidePanel = () => {
  const [moveItem] = useMoveItemMutation({
    refetchQueries: ["UnassignedScheduleItems"],
  });

  const { data, loading } = useUnassignedScheduleItemsQuery({
    variables: {
      code: "pycon2023",
    },
  });

  const [{ isOver, canDrop }, drop] = useDrop(
    () => ({
      accept: "item",
      drop: async (item: ScheduleItemFragment) => {
        console.log("drop", item);
        await moveItem({
          variables: {
            itemId: item.id,
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

  return (
    <div
      ref={drop}
      className="fixed p-4 border-l-4 bg-white top-0 right-0 h-full max-w-[200px] w-full overflow-x-scroll grid items-start content-start gap-3"
    >
      {loading && <div>Loading...</div>}
      {!loading &&
        data.unassignedScheduleItems.map((item) => (
          <BasketItem key={item.id} item={item} />
        ))}
    </div>
  );
};

const BasketItem = ({ item }: { item: ScheduleItemFragment }) => {
  const [{ opacity }, dragRef] = useDrag(
    () => ({
      type: "item",
      item: {
        ...item,
      },
      end: (item, monitor) => {
        if (monitor.didDrop()) {
          console.log("dropped");
        }
      },
      collect: (monitor) => ({
        opacity: monitor.isDragging() ? 0.5 : 1,
      }),
    }),
    [],
  );

  return <ItemCard ref={dragRef} item={item} />;
};
