import clsx from "clsx";
import React from "react";

type Props = React.InputHTMLAttributes<HTMLInputElement> & {
  checked: boolean;
};

export const Checkbox = ({ checked, ...props }: Props) => {
  return (
    <div className="relative w-14 h-7 md:h-10 md:w-20 shrink-0">
      <input
        type="checkbox"
        className={clsx(
          "w-full border border-black rounded-full h-full appearance-none transition-colors cursor-pointer",
          {
            "bg-cream": !checked,
            "bg-green": checked,
          }
        )}
        checked={checked}
        {...props}
      />
      <div
        className="w-7 h-7 md:w-10 md:h-10 bg-milk border border-black rounded-full absolute top-0 left-0 pointer-events-none transition-transform"
        style={{
          transform: checked ? `translateX(100%)` : `translateX(0)`,
        }}
      ></div>
    </div>
  );
};
