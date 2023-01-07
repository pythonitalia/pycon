import React from "react";
import { Textarea } from "./textarea";

export default {
  title: "Textarea",
  argTypes: {
    placeholder: {
      defaultValue: "",
      control: {
        type: "text",
      },
    },
    error: {
      defaultValue: "",
      control: {
        type: "text",
      },
    },
    rows: {
      defaultValue: 1,
      control: {
        type: "number",
      },
    },
  },
};

export const Primary = ({ placeholder, rows, error }) => {
  return (
    <div className="p-6">
      <Textarea placeholder={placeholder} rows={rows} errors={[error]} />
    </div>
  );
};
