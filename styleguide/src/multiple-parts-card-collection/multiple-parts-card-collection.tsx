import React from "react";

type Props = {
  children: React.ReactNode;
};

export const MultiplePartsCardCollection = ({ children }: Props) => {
  return <div className="multiple-parts-card-collection">{children}</div>;
};
