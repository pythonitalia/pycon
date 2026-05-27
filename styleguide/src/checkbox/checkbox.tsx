import clsx from "clsx";
import React from "react";

type Props = Omit<React.InputHTMLAttributes<HTMLInputElement>, "size"> & {
  checked: boolean;
  size?: "small" | "large";
};

export const Checkbox = ({ checked, size = "large", ...props }: Props) => {
  return (
    <div
      className={clsx("relative shrink-0", {
        "w-14.8 h-7.5 md:w-20 md:h-10": size === "large",
        "w-14.8 h-7.5": size === "small",
      })}
    >
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
        className={clsx(
          "bg-milk border border-black rounded-full absolute top-0 left-0 pointer-events-none transition-transform",
          {
            "w-7.5 h-7.5 md:w-10 md:h-10": size === "large",
            "w-7.5 h-7.5": size === "small",
          }
        )}
        style={{
          transform: checked ? `translateX(100%)` : `translateX(0)`,
        }}
      ></div>
    </div>
  );
};
