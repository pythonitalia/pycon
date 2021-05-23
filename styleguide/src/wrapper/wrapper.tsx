import React, { ReactNode } from "react";

export const Wrapper = ({ children }: { children: ReactNode }) => (
  <div className="max-w-7xl mx-auto px-8 py-8">{children}</div>
);
