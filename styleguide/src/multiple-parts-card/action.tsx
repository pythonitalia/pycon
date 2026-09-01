import React from "react";

import clsx from "clsx";

export const Action = ({
  children,
  button = false,
  noPadding = false,
  negative = false,
  onClick,
}: {
  button?: boolean;
  children: React.ReactNode;
  noPadding?: boolean;
  onClick?: () => void;
  negative?: boolean;
}) => {
  return (
    <div
      onClick={onClick}
      className={clsx(
        "flex items-center justify-center",
        "w-full",
        "transition-colors select-none",
        {
          "bg-caramel cursor-pointer": button,
          "hover:bg-green": button && !negative,
          "hover:bg-red": button && negative,
          "p-4 py-3.5 lg:px-5": !noPadding,
        }
      )}
    >
      {children}
    </div>
  );
};
