import React, { useState } from "react";

import { Select } from "./select";

export default {
  title: "Select",
  argTypes: {
    error: {
      defaultValue: "",
      control: {
        type: "text",
      },
    },
  },
};

export const Primary = ({ error }) => {
  const [value, setValue] = useState("");
  return (
    <div className="p-6">
      <Select
        required
        errors={[error]}
        value={value}
        onChange={(e) => setValue(e.target.value)}
      >
        <option disabled value="">
          Option #A
        </option>
        <option value="b">Option #B</option>
        <option value="c">Option #C</option>
      </Select>
    </div>
  );
};
