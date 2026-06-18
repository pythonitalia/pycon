import React from "react";
import { Button } from "../button/button";
import { Heading } from "../heading/index";
import { VerticalStack } from "./vertical-stack";

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
  <VerticalStack {...props}>
    <Heading>Long title to show aligns</Heading>

    <Button onClick={() => {}} color="pink">
      Button
    </Button>

    <Button onClick={() => {}} color="blue">
      Button
    </Button>
  </VerticalStack>
);
