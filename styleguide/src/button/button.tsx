import clsx from "clsx";
import React, { ReactNode } from "react";
import { Color } from "../types";
import { Text } from "../text";
import { getBackgroundClasses } from "../colors-utils";

export const Button = ({
  children,
  onClick,
  role = "primary",
  icon = null,
  size = "default",
  fullWidth = false,
  background,
  disabled = false,
  href = undefined,
  ...props
}: {
  background?: Color | "none";
  icon?: ReactNode;
  size?: "default" | "small";
  children: ReactNode;
  disabled?: boolean;
  role?: "primary" | "secondary" | "alert";
  onClick?: (
    e: React.MouseEvent<HTMLButtonElement> | React.MouseEvent<HTMLAnchorElement>
  ) => void;
  href?: string;
  fullWidth?: boolean | "mobile";
}) => {
  const Wrapper = href ? "a" : "button";
  return (
    <Wrapper
      {...props}
      disabled={disabled}
      className={clsx(
        "inline-flex items-center uppercase select-none border-black border cursor-pointer transition-colors",
        {
          "opacity-30": disabled,
          // primary
          "hover:bg-green": !disabled && role !== "alert",
          "hover:bg-red/40": !disabled && role === "alert",

          // secondary
          "bg-milk": role === "primary" && !background,
          "bg-cream": (role === "alert" || role === "secondary") && !background,
          ...(background ? getBackgroundClasses(background) : {}),

          "border-black": role !== "alert",
          "border-red": role === "alert",

          "py-5 px-8": size === "small",
          "py-5 px-8 lg:py-6 lg:px-12": size === "default",

          "justify-center md:justify-start": fullWidth === false,
          "justify-center w-full": fullWidth === true,
          "justify-center w-full lg:w-auto": fullWidth === "mobile",
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
        color={role === "alert" ? "red" : "black"}
      >
        {children}
      </Text>
    </Wrapper>
  );
};
