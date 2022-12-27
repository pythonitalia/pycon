import clsx from "clsx";
import React from "react";

type Props = {
  children: React.ReactNode;
  className?: string;
};

export const SideText = ({ children, className }: Props) => {
  return (
    <div
      className={clsx("px-4 py-3.5 lg:px-6 flex items-center gap-3", className)}
    >
      {children}
    </div>
  );
};
