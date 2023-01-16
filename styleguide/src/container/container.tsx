import clsx from "clsx";
import React from "react";

export type ContainerSize = "base" | "small" | "medium" | "2md";

type Props = React.PropsWithChildren<{
  className?: string;
  size?: ContainerSize;
  noPadding?: boolean;
  center?: boolean;
}>;

export const Container = ({
  noPadding = false,
  children,
  className,
  center = true,
  size = "base",
}: Props) => {
  return (
    <div
      className={clsx(
        "w-full",
        {
          "mx-auto": center,
          "max-w-container": size === "base",
          "max-w-container-small": size === "small",
          "max-w-container-medium": size === "medium",
          "max-w-container-2md": size === "2md",
          "px-4": !noPadding,
        },
        className
      )}
    >
      {children}
    </div>
  );
};
