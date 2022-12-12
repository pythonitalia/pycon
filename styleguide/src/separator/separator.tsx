import clsx from "clsx";
import React from "react";

type Props = {
  mobileOnly?: boolean;
  hidden?: boolean;
  escapeContainer?: boolean;
};

export const Separator = ({
  escapeContainer = false,
  hidden = false,
  mobileOnly = false,
}: Props) => (
  <div
    className={clsx("h-separator bg-black", {
      "lg:hidden": mobileOnly,
      hidden,
      "w-screen -ml-4": escapeContainer,
      "w-full": !escapeContainer,
    })}
  />
);
