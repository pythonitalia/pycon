import clsx from "clsx";
import React, { SVGProps } from "react";

type Props = SVGProps<SVGSVGElement> & {
  full?: boolean;
};

export const CloseIcon = (props: Props) => (
  <svg
    className={clsx({
      "w-8 h-8": !props.full,
      "w-full h-full": props.full,
    })}
    viewBox="0 0 33 33"
    fill="none"
  >
    <path
      fillRule="evenodd"
      clipRule="evenodd"
      d="M14.3483 16.5303L1.0901 29.7886L3.21142 31.9099L16.4697 18.6516L30.2583 32.4402L32.3796 30.3189L18.591 16.5303L32.9099 2.21142L30.7886 0.0900957L16.4697 14.409L2.68109 0.620426L0.559768 2.74175L14.3483 16.5303Z"
      fill="#0E1116"
    />
  </svg>
);
