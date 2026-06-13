import clsx from "clsx";
import React, { ReactNode } from "react";
import { getBackgroundClasses } from "../colors-utils";
import { Text } from "../text";
import { Color } from "../types";

export const Button = ({
  children,
  onClick,
  variant = "primary",
  icon = null,
  size = "default",
  fullWidth = false,
  background,
  disabled = false,
  href = undefined,
  target = undefined,
  ...props
}: {
  background?: Color | "none";
  icon?: ReactNode;
  size?: "default" | "small";
  children: ReactNode;
  disabled?: boolean;
  variant?: "primary" | "secondary" | "alert";
  onClick?: (
    e: React.MouseEvent<HTMLButtonElement> | React.MouseEvent<HTMLAnchorElement>
  ) => void;
  href?: string;
  target?: string;
  fullWidth?: boolean | "mobile";
}) => {
  const Wrapper = href ? "a" : "button";
  return (
    <Wrapper
      {...props}
      disabled={disabled}
      className={clsx(
        "inline-flex items-center uppercase select-none border-black border cursor-pointer transition-colors",
        background ? getBackgroundClasses(background) : "",
        {
          "opacity-30": disabled,
          // primary
          "hover:bg-green": !disabled && variant !== "alert",
          "hover:bg-red/40": !disabled && variant === "alert",

          // secondary
          "bg-milk": variant === "primary" && !background,
          "bg-cream": (variant === "alert" || variant === "secondary") && !background,

          "border-black": variant !== "alert",
          "border-red": variant === "alert",

          "py-5 px-8": size === "small",
          "py-5 px-8 lg:py-6 lg:px-12": size === "default",

          "justify-center md:justify-start": fullWidth === false,
          "justify-center w-full": fullWidth === true,
          "justify-center w-full md:w-auto md:justify-start":
            fullWidth === "mobile",
        }
      )}
      href={href}
      target={target}
      onClick={onClick}
    >
      {icon && <span className="mr-2">{icon}</span>}
      <Text
        noWrap
        weight="strong"
        size={size === "small" ? "label2" : "label1"}
        color={variant === "alert" ? "red" : "black"}
      >
        {children}
      </Text>
    </Wrapper>
  );
};
