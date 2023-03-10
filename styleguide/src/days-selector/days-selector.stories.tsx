import React, { useState } from "react";
import { DaysSelector } from "./days-selector";

export default {
  title: "Days Selector",
};

export const Primary = () => {
  const [selected, setSelected] = useState("2023-05-25");
  return (
    <DaysSelector
      language="en"
      days={[
        { date: "2023-05-25", selected: selected === "2023-05-25" },
        { date: "2023-05-26", selected: selected === "2023-05-26" },
        { date: "2023-05-27", selected: selected === "2023-05-27" },
        { date: "2023-05-28", selected: selected === "2023-05-28" },
      ]}
      onClick={(date) => {
        setSelected(date);
      }}
    >
      Text text
    </DaysSelector>
  );
};

export const CenteredSelector = () => {
  const [selected, setSelected] = useState("2023-05-25");
  return (
    <DaysSelector
      center={true}
      language="en"
      days={[
        { date: "2023-05-25", selected: selected === "2023-05-25" },
        { date: "2023-05-26", selected: selected === "2023-05-26" },
        { date: "2023-05-27", selected: selected === "2023-05-27" },
        { date: "2023-05-28", selected: selected === "2023-05-28" },
      ]}
      onClick={(date) => {
        setSelected(date);
      }}
    />
  );
};
