import clsx from "clsx";
import React from "react";

type Props = React.PropsWithChildren<{
  className?: string;
}>;

export const Container = ({ children, className }: Props) => {
  return (
    <div className={clsx("px-4 max-w-container mx-auto w-full", className)}>
      {children}
    </div>
  );
};
