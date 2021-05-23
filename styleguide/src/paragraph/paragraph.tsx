import clsx from "clsx";
import React, { ReactNode } from "react";

export const Paragraph = ({
  children,
  bold = false,
}: {
  children: ReactNode;
  bold?: boolean;
}) => (
  <p
    className={clsx("mb-8", {
      "font-bold": bold,
    })}
  >
    {children}
  </p>
);
