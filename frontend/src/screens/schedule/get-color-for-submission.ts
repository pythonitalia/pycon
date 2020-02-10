const COLOR_MAP = {
  beginner: "blue",
  intermediate: "orange",
  advanced: "keppel",
};

export const getColorForSubmission = (submission: {
  audienceLevel: { name: string };
}) =>
  COLOR_MAP[
    submission.audienceLevel.name.toLowerCase() as keyof typeof COLOR_MAP
  ];
