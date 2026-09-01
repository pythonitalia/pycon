import React from "react";

type Props = {
  children: React.ReactNode;
};

export const AvatarGroup = ({ children }: Props) => {
  return (
    <div className="flex [&>*]:-ml-4 [&>*:first-child]:ml-0">{children}</div>
  );
};
