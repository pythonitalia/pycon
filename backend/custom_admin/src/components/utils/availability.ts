export type AvailabilityValue = "preferred" | "available" | "unavailable";

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
