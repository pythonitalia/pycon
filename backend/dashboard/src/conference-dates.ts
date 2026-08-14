function parseConferenceDate(value: string) {
  const [year, month, day] = value.split("-").map(Number);
  return new Date(year, month - 1, day);
}

export function formatConferenceDate(value: string) {
  return new Intl.DateTimeFormat("en", {
    day: "numeric",
    month: "short",
  }).format(parseConferenceDate(value));
}

export function formatConferenceDateRange(
  startDate: string | null,
  endDate: string | null,
) {
  if (!startDate) {
    return "Dates to be announced";
  }

  const start = parseConferenceDate(startDate);
  const end = endDate ? parseConferenceDate(endDate) : start;
  const startMonth = new Intl.DateTimeFormat("en", { month: "short" }).format(
    start,
  );
  const endMonth = new Intl.DateTimeFormat("en", { month: "short" }).format(
    end,
  );

  if (start.getFullYear() === end.getFullYear()) {
    if (start.getMonth() === end.getMonth()) {
      return `${startMonth} ${start.getDate()}–${end.getDate()}, ${end.getFullYear()}`;
    }

    return `${startMonth} ${start.getDate()}–${endMonth} ${end.getDate()}, ${end.getFullYear()}`;
  }

  return `${startMonth} ${start.getDate()}, ${start.getFullYear()}–${endMonth} ${end.getDate()}, ${end.getFullYear()}`;
}
