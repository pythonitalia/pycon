import { useDrag } from "react-dnd";

import { Button, Tooltip } from "@radix-ui/themes";
import type { ScheduleItemFragmentFragment } from "../fragments/schedule-item.generated";
import { useDjangoAdminEditor } from "../shared/django-admin-editor-modal/context";
import type { AvailabilityValue } from "../utils/availability";
import { getSlotAvailabilityKey } from "../utils/availability";
import { convertHoursToMinutes } from "../utils/time";

// Only the primary speaker's availability is checked. Co-speakers are not asked
// for availability in the CFP form, so item.speakers is intentionally ignored here.
function getSpeakerAvailability(
  item: ScheduleItemFragmentFragment,
  date: string,
  slotHour: string,
): AvailabilityValue | null {
  const availabilities =
    item.proposal?.speaker?.participant?.speakerAvailabilities;
  if (!availabilities) return null;
  return availabilities[getSlotAvailabilityKey(date, slotHour)] ?? null;
}

const AVAILABILITY_BADGE: Record<
  AvailabilityValue,
  { bg: string; text: string; label: string }
> = {
  preferred: { bg: "#dcfce7", text: "#15803d", label: "★ Preferred" },
  available: { bg: "#dbeafe", text: "#1d4ed8", label: "✓ Available" },
  unavailable: { bg: "#fee2e2", text: "#b91c1c", label: "✗ Unavailable" },
};

function AvailabilityBadge({
  value,
}: { value: AvailabilityValue | undefined }) {
  if (!value) return <span style={{ color: "#9ca3af", fontSize: 11 }}>—</span>;
  const { bg, text, label } = AVAILABILITY_BADGE[value];
  return (
    <span
      style={{
        background: bg,
        color: text,
        fontSize: 11,
        fontWeight: 600,
        padding: "2px 7px",
        borderRadius: 999,
        whiteSpace: "nowrap",
      }}
    >
      {label}
    </span>
  );
}

function formatDate(dateStr: string) {
  const d = new Date(`${dateStr}T00:00:00`);
  return d.toLocaleDateString("en-GB", { month: "short", day: "numeric" });
}

function AvailabilityTooltipContent({
  availabilities,
}: { availabilities: Record<string, string> }) {
  const byDate: Record<
    string,
    { am?: AvailabilityValue; pm?: AvailabilityValue }
  > = {};
  for (const [key, value] of Object.entries(availabilities)) {
    const [date, period] = key.split("@");
    if (!byDate[date]) byDate[date] = {};
    byDate[date][period as "am" | "pm"] = value as AvailabilityValue;
  }
  const dates = Object.keys(byDate).sort();
  if (dates.length === 0) return <span>No availability data</span>;

  return (
    <div style={{ minWidth: 220, padding: "8px 4px" }}>
      <div
        style={{
          fontWeight: 700,
          fontSize: 12,
          marginBottom: 8,
          letterSpacing: "0.05em",
          textTransform: "uppercase",
          opacity: 0.7,
        }}
      >
        Speaker availability (half-day)
      </div>
      <div style={{ display: "flex", flexDirection: "column", gap: 6 }}>
        {dates.map((date) => (
          <div
            key={date}
            style={{
              display: "grid",
              gridTemplateColumns: "60px 1fr 1fr",
              alignItems: "center",
              gap: 8,
            }}
          >
            <span style={{ fontSize: 12, fontWeight: 600, opacity: 0.85 }}>
              {formatDate(date)}
            </span>
            <AvailabilityBadge value={byDate[date].am} />
            <AvailabilityBadge value={byDate[date].pm} />
          </div>
        ))}
      </div>
    </div>
  );
}

export const Item = ({
  slots,
  slot,
  item,
  rooms,
  rowStart,
  date,
}: {
  slots: any[];
  slot: any;
  item: ScheduleItemFragmentFragment;
  rooms: any[];
  rowStart: number;
  date: string;
}) => {
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
      <ScheduleItemCard
        item={item}
        duration={duration}
        date={date}
        slotHour={slot.hour}
      />
    </div>
  );
};

function SpeakerNames({ item }: { item: ScheduleItemFragmentFragment }) {
  const speakerNames = item.speakers.map((s) => s.fullname).join(", ");
  const availabilities =
    item.proposal?.speaker?.participant?.speakerAvailabilities;
  const hasAvailabilities =
    availabilities && Object.keys(availabilities).length > 0;

  if (!hasAvailabilities) {
    return <span>{speakerNames}</span>;
  }

  return (
    <Tooltip
      content={<AvailabilityTooltipContent availabilities={availabilities} />}
    >
      <span style={{ cursor: "help", borderBottom: "1px dotted currentColor" }}>
        {speakerNames}
      </span>
    </Tooltip>
  );
}

export const ScheduleItemCard = ({
  item,
  duration,
  date = null,
  slotHour = null,
}: {
  item: ScheduleItemFragmentFragment;
  duration: number | null;
  date?: string | null;
  slotHour?: string | null;
}) => {
  const availability =
    date && slotHour ? getSpeakerAvailability(item, date, slotHour) : null;
  const availabilities =
    item.proposal?.speaker?.participant?.speakerAvailabilities ?? {};
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
      {availability === "unavailable" && (
        <li className="mb-2 flex items-center gap-1.5 bg-amber-100 text-amber-800 border border-amber-300 text-xs font-semibold px-2 py-1 rounded">
          <span>⚠ Speaker unavailable</span>
          <Tooltip
            content={
              <AvailabilityTooltipContent availabilities={availabilities} />
            }
          >
            <span
              className="inline-flex items-center justify-center w-3.5 h-3.5 rounded-full bg-amber-400 text-amber-900 cursor-help leading-none"
              style={{ fontSize: 9, fontStyle: "italic", fontFamily: "serif" }}
            >
              i
            </span>
          </Tooltip>
        </li>
      )}
      <li>
        [{item.type} - {duration || "??"} mins]
      </li>
      <li>{item.status}</li>
      <li className="pt-2">
        <strong>{item.title}</strong>
      </li>
      {item.speakers.length > 0 && (
        <li>
          <SpeakerNames item={item} />
        </li>
      )}
      <li className="pt-2">
        <span>[TM: {item.talkManager?.fullname}]</span>
      </li>
      <li className="pt-2">
        <Button onClick={openEditLink}>Edit</Button>
      </li>
    </ul>
  );
};
