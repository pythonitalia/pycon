export const formatDeadlineDate = (datetime: string) => {
  const d = new Date(datetime);

  const formatter = new Intl.DateTimeFormat("en", {
    year: "numeric",
    month: "long",
    day: "numeric",
  });

  return formatter.format(d);
};

export const formatDeadlineTime = (datetime: string) => {
  const d = new Date(datetime);

  const formatter = new Intl.DateTimeFormat("en", {
    hour: "numeric",
    minute: "numeric",
    timeZoneName: "short",
  });

  return formatter.format(d);
};

export const formatDeadlineDateTime = (datetime: string) => {
  const d = new Date(datetime);

  const formatter = new Intl.DateTimeFormat("en", {
    year: "numeric",
    month: "long",
    day: "numeric",
    hour: "numeric",
    minute: "numeric",
    timeZoneName: "short",
  });

  return formatter.format(d);
};
