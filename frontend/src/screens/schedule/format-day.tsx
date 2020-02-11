export const formatDay = (day: string) => {
  const d = new Date(day);
  const formatter = new Intl.DateTimeFormat("default", {
    weekday: "long",
    day: "numeric",
    // TODO: use conference timezone
    timeZone: "Europe/Rome",
  });
  return formatter.format(d);
};
