import React from "react";
import { SideText } from "./sidetext";

type Props = {
  children: React.ReactNode;
  rightSide: React.ReactNode;
};

export const CardPartTwoSides = ({ children, rightSide }: Props) => (
  <div className="bg-milk grid md:grid-cols-cardpart-increments">
    <SideText>{children}</SideText>
    <SideText className="flex md:items-center">{rightSide}</SideText>
  </div>
);
