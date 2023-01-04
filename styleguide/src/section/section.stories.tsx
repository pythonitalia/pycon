import React from "react";
import { ContainerSize } from "../container/container";
import { Heading } from "../heading";
import { Text } from "../text";
import { Color } from "../types";
import { Section } from "./section";

export const Standard = ({
  containerSize = "base",
  background,
}: {
  containerSize: ContainerSize;
  background: Color | "none";
}) => {
  return (
    <Section containerSize={containerSize} background={background}>
      <Heading size={1}>Section!</Heading>
      <Text size={1}>Body Body Body Body Body Body Body Body</Text>
    </Section>
  );
};

export default {
  title: "Section",
  component: Standard,
  argTypes: {
    containerSize: {
      control: {
        type: "select",
        options: ["base", "medium"],
      },
      defaultValue: "base",
    },
    background: {
      defaultValue: "none",
      control: {
        type: "select",
        options: [
          "none",
          "coral",
          "caramel",
          "cream",
          "yellow",
          "green",
          "purple",
          "pink",
          "blue",
          "red",
          "success",
          "warning",
          "neutral",
          "black",
          "grey",
          "white",
          "milk",
        ],
      },
    },
  },
};
