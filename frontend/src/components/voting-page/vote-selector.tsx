/** @jsx jsx */
import { Box, Flex, Grid, Text } from "@theme-ui/components";
import { useCallback, useState } from "react";
import { jsx } from "theme-ui";

import { Star } from "../icons/star";

type Props = {
  className?: string;
  label?: string | React.ReactElement;
  onVote: (vote: number) => void;
  value: number;
};

const STARS = [1, 2, 3, 4, 5];

export const VoteSelector: React.SFC<Props> = ({
  className,
  onVote,
  value,
  label = "Vote",
}) => {
  const [hoverStar, setHoverStar] = useState(-1);
  const resetHover = useCallback(() => setHoverStar(-1), []);

  return (
    <Flex
      sx={{
        alignItems: "center",
        textTransform: "uppercase",
        userSelect: "none",
      }}
      className={className}
    >
      {label}
      <Flex
        as="ul"
        sx={{
          width: "100%",
          justifyContent: "space-between",
          listStyle: "none",
          ml: 4,
        }}
      >
        {STARS.map(starValue => (
          <li
            onMouseEnter={() => setHoverStar(starValue)}
            onMouseLeave={resetHover}
            sx={{
              cursor: "pointer",
            }}
            key={starValue}
            onClick={_ => onVote(starValue)}
          >
            <Star active={value >= starValue || starValue <= hoverStar} />
          </li>
        ))}
      </Flex>
    </Flex>
  );
};
