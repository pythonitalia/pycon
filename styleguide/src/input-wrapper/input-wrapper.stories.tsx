import React, { useState } from "react";

import { Input } from "../input";
import { InputWrapper } from "./input-wrapper";

export default {
  title: "Input Wrapper",
  argTypes: {
    title: {
      defaultValue: "Test Title",
      control: {
        type: "text",
      },
    },
    description: {
      defaultValue: "Test description",
      control: {
        type: "text",
      },
    },
    required: {
      defaultValue: false,
      control: {
        type: "boolean",
      },
    },
  },
};

export const Primary = ({ title, description, required }) => {
  const [value, setValue] = useState("");

  return (
    <div className="p-6">
      <InputWrapper title={title} description={description} required={required}>
        <Input
          placeholder="Test input"
          onChange={(e) => setValue(e.target.value)}
          value={value}
        />
      </InputWrapper>
    </div>
  );
};
