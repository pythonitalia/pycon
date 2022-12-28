import clsx from "clsx";
import React from "react";

export type ContainerSize = "base" | "medium";

type Props = React.PropsWithChildren<{
  className?: string;
  size?: ContainerSize;
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
          "max-w-container-medium": size === "medium",
          "px-4": !noPadding,
        },
        className
      )}
    >
      {children}
    </div>
  );
};
