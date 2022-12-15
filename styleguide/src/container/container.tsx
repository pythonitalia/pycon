import clsx from "clsx";
import React from "react";

type Props = React.PropsWithChildren<{
  className?: string;
  size?: "base";
  noPadding?: boolean;
}>;

export const Container = ({
  noPadding = false,
  children,
  className,
  size = "base",
}: Props) => {
  return (
    <div
      className={clsx(
        "mx-auto w-full",
        {
          "max-w-container": size === "base",
          "px-4": !noPadding,
        },
        className
      )}
    >
      {children}
    </div>
  );
};
