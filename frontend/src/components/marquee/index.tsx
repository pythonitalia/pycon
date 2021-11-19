/** @jsxRuntime classic */

/** @jsx jsx */
import { keyframes } from "@emotion/core";
import { useEffect, useState } from "react";
import { Flex, jsx, Text } from "theme-ui";

type MarqueeProps = {
  message: string;
};

const animation = keyframes`
  0% {
    transform: translateX(0);
  }
  100% {
    transform: translateX(-100%);
  }
`;

export const Marquee = ({ message }: MarqueeProps) => {
  const messageWithSeparator = `${message} / `;
  const ch = `${messageWithSeparator.length}ch`;
  // Huge number so that the SSR version doesn't show blank space at first render
  const [numOfShadows, setNumOfShadows] = useState(50);
  useEffect(() => {
    const listener = () => {
      setNumOfShadows(
        Math.ceil(
          window.innerWidth /
            (22.399993896484375 * messageWithSeparator.length),
        ),
      );
    };
    window.addEventListener("resize", listener);
    listener();
    return () => {
      window.removeEventListener("resize", listener);
    };
  }, []);

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
          animation: `${animation} 2.5s linear infinite`,
          width: `${ch}`,
          textShadow: new Array(numOfShadows)
            .fill(0)
            .map((_, i) => `calc(${ch} * ${i + 1}) 0 currentColor`)
            .join(","),
        }}
      >
        {messageWithSeparator}
      </Text>
    </Flex>
  );
};
