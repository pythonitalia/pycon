import clsx from "clsx";
import React from "react";

type Props = React.PropsWithChildren<{
  className?: string;
  size?: "base";
}>;

export const Container = ({ children, className, size = "base" }: Props) => {
  return (
    <div
      className={clsx(
        "px-4 mx-auto w-full",
        {
          "max-w-container": size === "base",
        },
        className
      )}
    >
      {children}
    </div>
  );
};
