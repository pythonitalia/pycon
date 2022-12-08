import clsx from "clsx";
import React, { SVGProps } from "react";

type Props = SVGProps<SVGSVGElement> & {
  full?: boolean;
};

export const MenuIcon = ({ full, ...props }: Props) => (
  <svg
    className={clsx({
      "w-8 h-8 lg:w-11 lg:h-7": !full,
      "h-full w-full": full,
    })}
    viewBox="0 0 44 27"
    fill="none"
    {...props}
  >
    <path
      fillRule="evenodd"
      clipRule="evenodd"
      d="M44 3H0V0H44V3ZM44 15H0V12H44V15ZM0 27H44V24H0V27Z"
      fill="#0E1116"
    />
  </svg>
);
