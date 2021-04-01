import React from "react";
import { Title } from "../title";

type Props = {
  title: string;
  children: React.ReactNode;
};

export const SplitSection = ({ title, children }: Props) => (
  <div className="border-t-4 border-b-4 border-black">
    <div className="max-w-7xl mx-auto md:grid md:grid-cols-2">
      <div className="p-8 md:p-16 border-black border-b-4 md:border-b-0 md:border-r-4">
        <Title>{title}</Title>

        {children}
      </div>
      <div className="p-8 md:p-16 relative"></div>
    </div>
  </div>
);
