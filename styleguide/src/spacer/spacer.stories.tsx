import React from "react";
import { Text } from "../text";
import { Spacer } from "./spacer";

export default {
  title: "Spacer",
  parameters: {
    layout: "centered",
  },
  argTypes: {
    size: {
      defaultValue: "medium",
      control: {
        type: "select",
        options: ["xs", "small", "medium", "2md", "large", "xl"],
      },
    },
    showOnlyOn: {
      defaultValue: undefined,
      control: {
        type: "select",
        options: ["", "mobile", "tablet", "desktop"],
      },
    },
  },
};

export const Primary = ({ size, showOnlyOn }) => (
  <>
    <Text>Block of text Block of text Block of text</Text>
    <Spacer showOnlyOn={showOnlyOn} size={size} />
    <Text>Block of text Block of text Block of text</Text>
  </>
);

export const Horizontal = ({ size, showOnlyOn }) => {
  return (
    <>
      <Text>Block of text Block of text Block of text</Text>
      <Spacer showOnlyOn={showOnlyOn} size={size} orientation="horizontal" />
      <Text>Block of text Block of text Block of text</Text>
    </>
  );
};
