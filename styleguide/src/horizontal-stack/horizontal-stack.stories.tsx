import React from "react";
import { Button } from "../button/button";
import { Heading } from "../heading";
import { HorizontalStack } from "./horizontal-stack";

export default {
  title: "Horizontal Stack",
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
  <HorizontalStack {...props}>
    <Heading>
      Long Title <br />
      With multiple <br />
      Lines in it
    </Heading>

    <Button onClick={() => {}} color="pink">
      Button
    </Button>

    <Button onClick={() => {}} color="blue">
      Button
    </Button>

    <Button onClick={() => {}} color="pink">
      Button
    </Button>

    <Button onClick={() => {}} color="blue">
      Button
    </Button>
  </HorizontalStack>
);
