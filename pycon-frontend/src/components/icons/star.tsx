/** @jsxRuntime classic */
/** @jsx jsx */

import React from "react";
import { jsx } from "theme-ui";

type Props = {
  active: boolean;
};

export const Star: React.SFC<Props> = ({ active }) => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    width="36"
    height="34"
    fill="none"
    viewBox="0 0 36 34"
  >
    <path
      stroke="#000"
      strokeWidth="2"
      d="M18 4l3.368 10.365h10.898l-8.817 6.405 3.368 10.365L18 24.73l-8.817 6.405 3.368-10.365-8.817-6.405h10.898L18 4z"
      fill={active ? "white" : ""}
    />
  </svg>
);
