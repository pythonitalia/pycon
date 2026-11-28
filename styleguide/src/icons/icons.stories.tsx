import React, { useState } from "react";
import { HeartIcon } from "./heart";
import { LiveIcon } from "./live";
import { LiveCircleIcon } from "./live-circle";

export default {
  title: "Icons",
  parameters: {
    layout: "centered",
  },
};

export const Primary = () => {
  const [fill, setToggleFill] = useState(false);
  return (
    <div>
      <HeartIcon
        filled={fill}
        onClick={() => setToggleFill((value) => !value)}
      />
      <LiveIcon />
      Live circle:
      <div className="bg-red p-3">
        <LiveCircleIcon />
      </div>
    </div>
  );
};
