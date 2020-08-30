import { Language } from "~/locale/get-initial-locale";

export const formatDay = (day: string, language: Language) => {
  const d = new Date(day);
  const formatter = new Intl.DateTimeFormat(language, {
    weekday: "long",
    day: "numeric",
    // TODO: use conference timezone
    timeZone: "Europe/Rome",
  });
  return formatter.format(d);
};
