/** @jsxRuntime classic */

/** @jsx jsx */
import { keyframes } from "@emotion/core";
import { useEffect, useState } from "react";
import { Flex, jsx, Text } from "theme-ui";

type MarqueeProps = {
  message: string;
  separator?: string;
};

const animation = keyframes`
  0% {
    transform: translateX(0);
  }
  100% {
    transform: translateX(-100%);
  }
`;

// This is the font width of the character 0 at the font size of 32px
// It should be roughly the same as a CSS 1ch value.
// To calculate it I used this solution: https://stackoverflow.com/a/21015393
// getTextWidth("0", getCanvasFontSize(el))
// Where el must be the marquee text
const WIDTH_OF_0_FOR_MARQUEE_SIZE = 22.4;

export const Marquee = ({ message, separator = "/" }: MarqueeProps) => {
  const countSeparator = message.length > 13;
  const messageWithSeparator = countSeparator
    ? `${message} ${separator}`
    : `${message}`;
  const ch = `${messageWithSeparator.length}ch`;
  // Huge number so that the SSR version doesn't show blank space at first render
  const [numOfShadows, setNumOfShadows] = useState(50);
  useEffect(() => {
    const listener = () => {
      // Since our text is at a fixed font size and doesn't increase/decrease
      // with the width of the screen, we need to manually calculate how many
      // text shadows we think we will need to cover the entire screen
      setNumOfShadows(
        Math.ceil(
          window.innerWidth /
            (WIDTH_OF_0_FOR_MARQUEE_SIZE * messageWithSeparator.length),
        ),
      );
    };
    // We want to replace the crazy high value added to avoid blank space due to SSR
    // with a real value from the browser
    listener();

    window.addEventListener("resize", listener);
    return () => {
      window.removeEventListener("resize", listener);
    };
  }, [message]);

  return (
    <Flex
      sx={{
        height: 125,
        alignItems: "center",
        borderTop: "primary",
        borderBottom: "primary",
      }}
    >
      <Text
        as="span"
        variant="marquee"
        sx={{
          display: "inline-block",
          whiteSpace: "nowrap",
          willChange: "transform",
          animation: `${animation} ${
            5000 * (message.length * 0.1)
          }ms linear infinite`,
          width: ch,
          textShadow: new Array(numOfShadows)
            .fill(0)
            .map((_, i) => `calc(${ch} * ${i + 1}) 0 currentColor`)
            .join(","),
          userSelect: "none",
          "&:after": {
            content: `'${separator}'`,
            m: "0 7px",
          },
        }}
        css={`
          @media (prefers-reduced-motion: reduce) {
            animation: none !important;
          }
        `}
      >
        {message}
      </Text>
    </Flex>
  );
};
