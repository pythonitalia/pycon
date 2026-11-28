import clsx from "clsx";
import * as React from "react";

type Props = React.SVGProps<SVGSVGElement> & {
  filled?: boolean;
  onClick?: React.MouseEventHandler<SVGSVGElement>;
};

export const HeartIcon = ({ filled = false, onClick, ...props }: Props) => {
  return (
    <svg
      width={23}
      height={21}
      viewBox="0 0 23 21"
      className={clsx({
        "fill-coral": filled,
        "fill-none": !filled,
        "cursor-pointer": !!onClick,
      })}
      onClick={onClick}
      {...props}
    >
      <path
        d="M20.291 2.612a5.5 5.5 0 00-7.78 0l-1.06 1.06-1.06-1.06a5.501 5.501 0 00-7.78 7.78l1.06 1.06 7.78 7.78 7.78-7.78 1.06-1.06a5.5 5.5 0 000-7.78v0z"
        stroke="#0E1116"
        strokeWidth={2}
        strokeLinecap="round"
      />
    </svg>
  );
};
