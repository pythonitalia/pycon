import { Language } from "~/locale/get-initial-locale";

export const formatDeadlineDate = (datetime: string, language: Language) => {
  const d = new Date(datetime);

  const formatter = new Intl.DateTimeFormat(language, {
    year: "numeric",
    month: "long",
    day: "numeric",
  });

  return formatter.format(d);
};

export const formatDeadlineTime = (datetime: string, language: Language) => {
  const d = new Date(datetime);

  const formatter = new Intl.DateTimeFormat(language, {
    hour: "numeric",
    minute: "numeric",
    timeZoneName: "short",
  });

  return formatter.format(d);
};
