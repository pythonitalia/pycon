import clsx from "clsx";
import React from "react";
import { getTextColorClasses } from "../colors-utils";
import { Color } from "../types";

type Props = {
  children: React.ReactNode;
  href: string;
  rel?: string;
  color?: Color;
  target?: string;
  hoverColor?: Color;
  noHover?: boolean;
  noLayout?: boolean;
  onClick?: (e: React.MouseEvent<HTMLAnchorElement, MouseEvent>) => void;
  className?: string;
};

export const Link = ({
  href,
  children,
  rel,
  target,
  color = "black",
  hoverColor = "green",
  noHover = false,
  noLayout = false,
  onClick,
  className,
}: Props) => {
  return (
    <a
      onClick={onClick}
      className={clsx(
        "transition-colors fill-current",
        {
          ...getTextColorClasses(color),

          "hover:text-coral": hoverColor === "coral" && !noHover,
          "hover:text-caramel": hoverColor === "caramel" && !noHover,
          "hover:text-cream": hoverColor === "cream" && !noHover,
          "hover:text-yellow": hoverColor === "yellow" && !noHover,
          "hover:text-green": hoverColor === "green" && !noHover,
          "hover:text-purple": hoverColor === "purple" && !noHover,
          "hover:text-pink": hoverColor === "pink" && !noHover,
          "hover:text-blue": hoverColor === "blue" && !noHover,
          "hover:text-red": hoverColor === "red" && !noHover,
          "hover:text-success": hoverColor === "success" && !noHover,
          "hover:text-warning": hoverColor === "warning" && !noHover,
          "hover:text-neutral": hoverColor === "neutral" && !noHover,
          "hover:text-black": hoverColor === "black" && !noHover,
          "hover:text-white": hoverColor === "white" && !noHover,
          "hover:text-milk": hoverColor === "milk" && !noHover,

          contents: noLayout,
        },
        className
      )}
      href={href}
      rel={rel}
      target={target}
    >
      {children}
    </a>
  );
};
