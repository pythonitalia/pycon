import * as React from "react";

export const DrinkIcon = (props: React.SVGProps<SVGSVGElement>) => {
  return (
    <svg width={48} height={48} viewBox="0 0 48 48" fill="none" {...props}>
      <g clipPath="url(#prefix__clip0_1088_28892)">
        <path d="M0 0h48v48H0z" />
        <path
          d="M44.308 5H4l20.308 16.462L44.308 5zM24.46 21.308v21.538"
          stroke="#0E1116"
          strokeWidth={3}
        />
        <path
          d="M12.305 43H36.15"
          stroke="#0E1116"
          strokeWidth={3}
          strokeLinecap="round"
        />
      </g>
      <defs>
        <clipPath id="prefix__clip0_1088_28892">
          <path fill="#fff" d="M0 0h48v48H0z" />
        </clipPath>
      </defs>
    </svg>
  );
};
