import React from "react";
import { IntermissionText } from ".";

export const Standard = ({ text, ...props }) => (
  <div className="bg-purple h-screen w-screen p-4">
    <IntermissionText {...props}>{text}</IntermissionText>
  </div>
);

export default {
  title: "Livestream intermission text",

  argTypes: {
    text: {
      defaultValue: "Stream starting soon...",
      control: {
        type: "text",
      },
    },
  },
};
