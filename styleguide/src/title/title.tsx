import React, { ReactNode } from "react";

export const Title = ({ children }: { children: ReactNode }) => (
  <h1 className="font-medium text-5xl mb-8">{children}</h1>
);
