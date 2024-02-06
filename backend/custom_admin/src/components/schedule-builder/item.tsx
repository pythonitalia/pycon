import { useApolloClient } from "@apollo/client";

import { convertHoursToMinutes } from "../utils/time";
import { useIframeEditor } from "./context";

export const Item = ({ slots, slot, item, rooms, rowStart }) => {
  const apolloClient = useApolloClient();
  const roomIndexes = item.rooms
    .map((room) => rooms.findIndex((r) => r.id === room.id))
    .sort();

  const start = convertHoursToMinutes(slot.hour);
  const duration = item.duration || slot.duration || item.submission?.duration;

  const end = start + duration;

  const currentSlotIndex = slots.findIndex((s) => s.id === slot.id);

  let endingSlotIndex = slots.findIndex(
    (s) => convertHoursToMinutes(s.hour) + s.duration > end,
  );

  if (endingSlotIndex === -1) {
    endingSlotIndex = slots.length;
  }

  const index = roomIndexes[0];
  const { open } = useIframeEditor();

  const openEditLink = (e) => {
    e.preventDefault();

    open(item.id);
  };

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
      <ul>
        <li>[{item.type}]</li>
        <li>{item.title}</li>
        <li>
          <strong>Duration</strong>:{" "}
          <span>{item.submission?.duration} mins</span>
        </li>
        <li>
          <strong>Speakers</strong>:{" "}
          <span>
            {item.speakers.map((speaker) => speaker.fullname).join(",")}
          </span>
        </li>
        <li>
          <a className="underline" href="#" onClick={openEditLink}>
            Edit schedule item!!
          </a>
        </li>
      </ul>
    </div>
  );
};
