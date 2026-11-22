const SCORE_COLORS = ["green", "lime", "amber", "orange", "red"] as const;

export const scoreColor = (index: number, total: number) =>
  SCORE_COLORS[
    total < 2
      ? 0
      : Math.round((index / (total - 1)) * (SCORE_COLORS.length - 1))
  ];
