import clsx from "clsx";
import React, { SVGProps } from "react";

type Props = SVGProps<SVGSVGElement> & {
  full?: boolean;
};

export const TicketsIcon = ({ full, ...props }: Props) => (
  <svg
    className={clsx({
      "h-full w-full": full,
      "w-6 h-7 lg:w-9 lg:h-11": !full,
    })}
    viewBox="0 0 36 42"
    fill="none"
    {...props}
  >
    <path
      fillRule="evenodd"
      clipRule="evenodd"
      d="M0 0L0 3L0 39L0 42H3H12.189C12.8551 39.4122 15.2042 37.5 18 37.5C20.7958 37.5 23.1449 39.4122 23.811 42H33H36V39V3V0L33 0L23.811 0C23.1449 2.58784 20.7958 4.5 18 4.5C15.2042 4.5 12.8551 2.58784 12.189 0L3 0L0 0ZM10.205 39H3L3 22.5H8.5V19.5H3L3 3L10.205 3C11.7605 5.6893 14.6664 7.5 18 7.5C21.3336 7.5 24.2395 5.6893 25.795 3L33 3V19.5L27.5 19.5V22.5L33 22.5V39H25.795C24.2395 36.3107 21.3336 34.5 18 34.5C14.6664 34.5 11.7605 36.3107 10.205 39ZM13.5 22.5V19.5H22.5V22.5H13.5Z"
      fill="#0E1116"
    />
  </svg>
);
