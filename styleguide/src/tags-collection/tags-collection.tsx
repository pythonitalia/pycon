import React from "react";

type Props = {
  children: React.ReactNode;
};
export const TagsCollection = ({ children }: Props) => {
  return <div className="flex gap-2 flex-wrap">{children}</div>;
};
