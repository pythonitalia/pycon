import { Language } from "~/locale/get-initial-locale";

export const formatDay = (
  day: string,
  language: Language,
  timezone: string,
) => {
  const d = new Date(day);
  const formatter = new Intl.DateTimeFormat(language, {
    weekday: "long",
    day: "numeric",
    timeZone: timezone,
  });
  return formatter.format(d);
};
