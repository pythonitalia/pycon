import React from "react";
import { Countdown } from "./countdown";

export const Standard = ({
  deadline,
  snakeLookingAt,
  showSnake,
  background,
}) => (
  <Countdown
    deadline={deadline}
    snakeLookingAt={snakeLookingAt}
    showSnake={showSnake}
    background={background}
  />
);

export default {
  title: "Countdown",
  component: Standard,
  argTypes: {
    deadline: {
      control: {
        type: "date",
      },
    },
    showSnake: {
      control: {
        type: "boolean",
      },
    },
    background: {
      control: {
        type: "select",
        defaultValue: "green",
        options: ["green", "blue", "red", "yellow", "cream"],
      },
    },
    snakeLookingAt: {
      control: {
        type: "select",
        defaultValue: "left",
        options: ["left", "right"],
      },
    },
  },
};
