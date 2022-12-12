import React from "react";
import { SnakeCountdown } from "./snake-countdown";

export const Standard = ({ deadline, snakeLookingAt }) => (
  <SnakeCountdown deadline={deadline} snakeLookingAt={snakeLookingAt} />
);

export default {
  title: "Snake countdown",
  component: Standard,
  argTypes: {
    deadline: {
      control: {
        type: "date",
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
