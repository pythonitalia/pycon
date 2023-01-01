import clsx from "clsx";
import React, { ReactNode } from "react";
import { Color } from "../types";
import { Text } from "../text";

export const Button = ({
  children,
  onClick,
  role = "primary",
  icon = null,
  size = "default",
  fullWidth = false,
  color = "white",
  disabled = false,
  href = undefined,
}: {
  color?: Color;
  icon?: ReactNode;
  size?: "default" | "small";
  children: ReactNode;
  disabled?: boolean;
  role?: "primary" | "secondary";
  onClick?: (
    e: React.MouseEvent<HTMLButtonElement> | React.MouseEvent<HTMLAnchorElement>
  ) => void;
  href?: string;
  fullWidth?: boolean;
}) => {
  const Wrapper = href ? "a" : "button";
  return (
    <Wrapper
      disabled={disabled}
      className={clsx(
        "inline-flex items-center uppercase select-none border-black border cursor-pointer transition-colors",
        {
          "opacity-30": disabled,
          // primary
          "hover:bg-green": !disabled,
          // secondary
          "bg-milk": role === "primary",
          "bg-cream": role === "secondary",

          "py-5 px-8": size === "small",
          "py-5 px-8 lg:py-6 lg:px-12": size === "default",

          "justify-center md:justify-start w-full md:w-auto": !fullWidth,
          "justify-center w-full": fullWidth,
        }
      )}
      href={href}
      onClick={onClick}
    >
      {icon && <span className="mr-2">{icon}</span>}
      <Text
        noWrap
        weight="strong"
        size={size === "small" ? "label2" : "label1"}
      >
        {children}
      </Text>
    </Wrapper>
  );
};
