import React from "react";

export const ItalianIcon: React.SFC<{ active: boolean }> = ({
  active,
  ...props
}) => (
  <svg viewBox="0 0 50 50" fill="none" {...props}>
    <g clipPath="url(#prefix__clip0)">
      <path
        d="M50 25c0 13.806-11.194 25-25 25C11.193 50 0 38.807 0 25S11.193 0 25 0s25 11.193 25 25z"
        fill="#F0F0F0"
      />
      <path
        d="M50 25c0-10.75-6.784-19.912-16.305-23.445v46.89C43.215 44.913 50 35.749 50 25z"
        fill="#D80027"
      />
      <path
        d="M0 25c0 10.748 6.785 19.912 16.305 23.445V1.555C6.785 5.088 0 14.251 0 25z"
        fill="#6DA544"
      />
      <circle cx={25} cy={25} r={23} stroke="#000" strokeWidth={4} />
      {active && (
        <circle cx={25} cy={25} r={19} stroke="#fff" strokeWidth={4} />
      )}
    </g>
    <defs>
      <clipPath id="prefix__clip0">
        <path fill="#fff" d="M0 0h50v50H0z" />
      </clipPath>
    </defs>
  </svg>
);
