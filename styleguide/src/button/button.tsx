import clsx from "clsx";
import React, { ReactNode } from "react";
import { Color } from "../types";
import { Text } from "../text";

export const Button = ({
  children,
  onClick,
  role = "primary",
  icon = null,
  color = "white",
  disabled = false,
}: {
  color?: Color;
  icon?: ReactNode;
  children: ReactNode;
  disabled?: boolean;
  role?: "primary" | "secondary";
  onClick: () => void;
}) => (
  <button
    disabled={disabled}
    className={clsx(
      "flex items-center justify-center md:justify-start uppercase border-black border-3 py-5 px-8 w-full md:w-auto lg:py-6 lg:px-12",
      {
        "opacity-30": disabled,
        // primary
        "hover:bg-green": !disabled,
        // secondary
        "bg-cream": role === "secondary",
      }
    )}
    onClick={onClick}
  >
    {icon && <span className="mr-2">{icon}</span>}
    <Text weight="strong" size="label1">
      {children}
    </Text>
  </button>
);
