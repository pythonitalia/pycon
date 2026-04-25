import React, { useState } from "react";
import { Select } from "../select";

import { Input } from "../input";
import { InputWrapper } from "./input-wrapper";
import { Textarea } from "../textarea";

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

export const FormExample = ({ title, description, required }) => {
  const [value, setValue] = useState("");
  const [selectValue, setSelectValue] = useState("");
  const [textareaValue, setTextareaValue] = useState("");

  return (
    <div className="p-6">
      <InputWrapper title={title} description={description} required={required}>
        <Input
          placeholder="Test input"
          onChange={(e) => setValue(e.target.value)}
          value={value}
        />
      </InputWrapper>

      <InputWrapper title={title} description={description} required={required}>
        <Select
          placeholder="Test Select"
          onChange={(e) => setSelectValue(e.target.value)}
          value={selectValue}
        >
          <option value="1">Test 1</option>
          <option value="2">Test 2</option>
          <option value="3">Test 3</option>
        </Select>
      </InputWrapper>

      <InputWrapper title={title} description={description} required={required}>
        <Textarea
          value={textareaValue}
          placeholder="Test textarea"
          onChange={(e) => setTextareaValue(e.target.value)}
        />
      </InputWrapper>
    </div>
  );
};
