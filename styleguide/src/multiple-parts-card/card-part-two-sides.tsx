import React from "react";
import { SideText } from "./sidetext";

type Props = {
  children: React.ReactNode;
  rightSide: React.ReactNode;
};

export const CardPartTwoSides = ({ children, rightSide }: Props) => (
  <div className="bg-cream grid md:grid-cols-cardpart-increments">
    <SideText>{children}</SideText>
    <SideText className="flex items-center md:justify-center">
      {rightSide}
    </SideText>
  </div>
);
