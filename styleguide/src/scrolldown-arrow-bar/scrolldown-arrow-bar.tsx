import React from "react";

export const ScrollDownArrowBar = () => {
  return (
    <div className="relative overflow-x-clip">
      <LineArrow />
      <div className="bg-coral absolute top-[39px] w-full h-[60px]"></div>
    </div>
  );
};

const LineArrow = () => (
  <svg width="100%" height="100" fill="#F17A5D" className="relative z-10">
    <defs>
      <pattern
        id="scrolldownarrowbar"
        patternUnits="userSpaceOnUse"
        width="33"
        height="4"
        viewBox="0 0 33 4"
      >
        <path
          d="M2 2H10.2632H15.8901H21.517H31"
          stroke="#0E1116"
          strokeWidth="4"
          strokeLinecap="square"
          strokeLinejoin="round"
        />
      </pattern>
    </defs>
    <path
      d="M2 39.5H78.5849C96.9181 39.5 114.643 32.9256 128.542 20.9705V20.9705C157.266 -3.73551 199.734 -3.73551 228.458 20.9705V20.9705C242.357 32.9256 260.082 39.5 278.415 39.5H370.5"
      stroke="#0E1116"
      strokeWidth="4"
      strokeLinecap="round"
      strokeLinejoin="round"
    />
    <path
      d="M178.001 30.3008V71.533M178.001 71.533L157.766 51.2974M178.001 71.533L198.237 51.2974"
      stroke="#0E1116"
      strokeWidth="4"
      strokeLinecap="round"
      strokeLinejoin="round"
    />
    <rect
      x="370"
      y="37.5"
      width="100%"
      height="4"
      fill="url(#scrolldownarrowbar)"
    />
  </svg>
);
