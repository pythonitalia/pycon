import { useState } from "react";

import { useInterval } from "~/helpers/use-interval";

export const AnimatedEmoji = ({ play }: { play: boolean }) => {
  const clocks = [
    "🕐",
    "🕑",
    "🕒",
    "🕓",
    "🕔",
    "🕕",
    "🕖",
    "🕗",
    "🕘",
    "🕙",
    "🕚",
    "🕛",
  ];

  const [count, setCount] = useState(0);

  useInterval(
    () => {
      setCount(count + 1);
    },
    play ? 100 : null,
  );
  return clocks[count % clocks.length];
};
