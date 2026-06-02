export type AvailabilityValue = "preferred" | "available" | "unavailable";

// Single source of truth for how each availability value is presented.
// Both the inline-styled tooltip badge (item.tsx) and the Radix Badge
// (proposal-preview.tsx) read from here, so adding a new AvailabilityValue
// forces updating one map and the Record type stays exhaustive.
export const AVAILABILITY_META: Record<
  AvailabilityValue,
  {
    label: string;
    glyph: string;
    color: "green" | "blue" | "red";
    bg: string;
    text: string;
  }
> = {
  preferred: {
    label: "Preferred",
    glyph: "★",
    color: "green",
    bg: "#dcfce7",
    text: "#15803d",
  },
  available: {
    label: "Available",
    glyph: "✓",
    color: "blue",
    bg: "#dbeafe",
    text: "#1d4ed8",
  },
  unavailable: {
    label: "Unavailable",
    glyph: "✗",
    color: "red",
    bg: "#fee2e2",
    text: "#b91c1c",
  },
};

// Availability is stored at half-day granularity: "am" (before 12:00) or "pm" (12:00 and after).
// A slot at 09:00 and one at 11:30 map to the same "am" bucket. The badge reflects the
// half-day preference, not the exact start time of the slot.
export function getSlotAvailabilityKey(
  dayDate: string,
  slotHour: string,
): string {
  const hour = Number.parseInt(slotHour.split(":")[0], 10);
  const period = hour < 12 ? "am" : "pm";
  return `${dayDate}@${period}`;
}
