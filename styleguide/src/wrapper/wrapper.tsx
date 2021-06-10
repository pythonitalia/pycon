import clsx from "clsx";
import React, { ReactNode } from "react";

type Props = {
  center?: boolean;
  children: ReactNode;
};

export const Wrapper = ({ children, center = false }: Props) => (
  <div
    className={clsx("max-w-7xl mx-auto px-8 py-8", {
      "flex items-center justify-center": center,
    })}
  >
    {children}
  </div>
);
