import { Item } from "./types";

const COLOR_MAP = {
  beginner: "blue",
  intermediate: "orange",
  advanced: "keppel",
  custom: "cinderella",
};

export const getColorForSubmission = (submission: {
  audienceLevel: { name: string } | null;
}) =>
  COLOR_MAP[
    submission.audienceLevel!.name.toLowerCase() as keyof typeof COLOR_MAP
  ];

export const getColorForItem = (item: Item) => {
  if (item.audienceLevel) {
    return COLOR_MAP[
      item.audienceLevel.name.toLowerCase() as keyof typeof COLOR_MAP
    ];
  }

  if (item.submission) {
    return getColorForSubmission(item.submission);
  }

  return COLOR_MAP.custom;
};
