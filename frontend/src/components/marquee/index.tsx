/** @jsx jsx */
import { keyframes } from "@emotion/core";
import { Flex, Text } from "@theme-ui/components";
import { jsx } from "theme-ui";

type MarqueeProps = {
  message: string;
};

const animation = keyframes`
  0% { transform: translate(0, 0); }
  100% { transform: translate(-100%, 0); }
`;

export const Marquee: React.SFC<MarqueeProps> = ({ message }) => (
  <Flex
    sx={{
      overflow: "hidden",
      alignItems: "center",
      height: 125,
      borderTop: "primary",
      borderBottom: "primary",
    }}
  >
    <Text
      variant="marquee"
      sx={{
        willChange: "transform",
        animation: `${animation} 20s linear infinite`,
      }}
    >
      {new Array(10).fill(message).join(" / ")}
    </Text>
  </Flex>
);
