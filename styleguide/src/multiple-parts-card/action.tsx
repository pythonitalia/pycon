import React from "react";

import clsx from "clsx";

export const Action = ({
  children,
  button = false,
  noPadding = false,
  noBorderMobile = false,
  breakpoint = "md",
  negative = false,
  onClick,
}: {
  button?: boolean;
  children: React.ReactNode;
  noPadding?: boolean;
  noBorderMobile?: boolean;
  breakpoint?: "md" | "lg";
  onClick?: () => void;
  negative?: boolean;
}) => {
  return (
    <div
      onClick={onClick}
      className={clsx(
        "border-t last:border-r-0",
        "flex items-center justify-center",
        "w-full",
        "transition-colors select-none",
        {
          "bg-caramel cursor-pointer": button,
          "hover:bg-green": button && !negative,
          "hover:bg-red": button && negative,
          "p-4 py-3.5 lg:px-5": !noPadding,

          "border-r": !noBorderMobile,

          "md:w-auto md:border-r-0 md:border-t-0 md:border-l":
            breakpoint === "md",
          "lg:w-auto lg:border-r-0 lg:border-t-0 lg:border-l":
            breakpoint === "lg",
        }
      )}
    >
      {children}
    </div>
  );
};
