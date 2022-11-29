import React from "react";
import { Button } from "../button/button";
import { Title } from "../title";
import { HStack } from "./hstack";

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
  <HStack {...props}>
    <Title>
      Long Title <br />
      With multiple <br />
      Lines in it
    </Title>

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
  </HStack>
);
