import React, { ReactNode } from "react";

type Props = {
  children: ReactNode;
};

export const Wrapper = ({ children }: Props) => (
  <div className="px-8 py-8 mx-auto max-w-7xl">{children}</div>
);
