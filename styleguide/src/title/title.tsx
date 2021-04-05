import clsx from "clsx";
import React, { ReactNode } from "react";

export const Title = ({
  children,
  marginBottom = true,
}: {
  children: ReactNode;
  marginBottom?: boolean;
}) => (
  <h1
    className={clsx("font-medium text-2xl leading-loose md:text-5xl", {
      "mb-8": marginBottom,
    })}
  >
    {children}
  </h1>
);
