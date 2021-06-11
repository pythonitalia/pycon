import React from "react";
import { Button } from "../button/button";
import { Title } from "../title";
import { VStack } from "./vstack";

export default {
  title: "Vertical Stack",
  argTypes: {
    align: {
      defaultValue: "left",
      control: {
        type: "select",
        options: ["left", "center", "right"],
      },
    },
  },
  parameters: {
    layout: "centered",
  },
};

export const Primary = (props) => (
  <VStack {...props}>
    <Title>Long title to show aligns</Title>

    <Button onClick={() => {}} color="pink">
      Button
    </Button>

    <Button onClick={() => {}} color="aquamarine">
      Button
    </Button>
  </VStack>
);
