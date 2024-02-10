import { useDrag } from "react-dnd";

import { useDjangoAdminEditor } from "../shared/django-admin-editor-modal/context";
import { convertHoursToMinutes } from "../utils/time";

export const Item = ({ slots, slot, item, rooms, rowStart }) => {
  const roomIndexes = item.rooms
    .map((room) => rooms.findIndex((r) => r.id === room.id))
    .sort();

  const start = convertHoursToMinutes(slot.hour);
  const duration =
    item.duration || slot.duration || item.proposal?.duration.duration;

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
      className="z-50 bg-slate-200"
    >
      <ScheduleItemCard item={item} duration={duration} />
    </div>
  );
};

export const ScheduleItemCard = ({ item, duration }) => {
  const [{ opacity }, dragRef] = useDrag(
    () => ({
      type: "scheduleItem",
      item: {
        item,
      },
      collect: (monitor) => ({
        opacity: monitor.isDragging() ? 0.5 : 1,
      }),
    }),
    [],
  );
  const { open } = useDjangoAdminEditor();

  const openEditLink = (e) => {
    e.preventDefault();
    open(`/schedule/scheduleitem/${item.id}/change`);
  };

  return (
    <ul className="bg-slate-200 p-3" ref={dragRef}>
      <li>
        [{item.type} - {duration || "??"} mins]
      </li>
      <li>{item.status}</li>
      <li className="pt-2">
        <strong>{item.title}</strong>
      </li>
      {item.speakers.length > 0 && (
        <li>
          <span>
            {item.speakers.map((speaker) => speaker.fullname).join(",")}
          </span>
        </li>
      )}
      <li className="pt-2">
        <a className="underline" href="#" onClick={openEditLink}>
          Edit schedule item
        </a>
      </li>
    </ul>
  );
};
