import React, { useState } from "react";
import { InputNumber } from "./input-number";

export default {
  title: "Input Number",
};

const VALUES = [
  { value: "1", label: "Didn't like it" },
  { value: "2", label: "Ok" },
  { value: "3", label: "I like it" },
  { value: "4", label: "Was amazing!" },
];

export const Primary = () => {
  const [value, setValue] = useState("");
  const [selected, setSelected] = useState("4");

  return (
    <div className="bg-blue">
      <div className="p-6">
        <InputNumber values={VALUES} value={value} onClick={setValue} />
      </div>
      <div className="p-6">
        <InputNumber values={VALUES} value={selected} onClick={setSelected} />
      </div>
    </div>
  );
};
