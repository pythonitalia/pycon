import clsx from "clsx";
import React from "react";
import { Color } from "../types";

type Props = React.PropsWithChildren<{
  href: string;
  rel?: string;
  target?: string;
  hoverColor?: Color;
}>;

export const Link = ({
  href,
  children,
  rel,
  target,
  hoverColor = "green",
}: Props) => {
  return (
    <a
      className={clsx("text-black hover:fill-current transition-colors", {
        "hover:text-coral": hoverColor === "coral",
        "hover:text-caramel": hoverColor === "caramel",
        "hover:text-cream": hoverColor === "cream",
        "hover:text-yellow": hoverColor === "yellow",
        "hover:text-green": hoverColor === "green",
        "hover:text-purple": hoverColor === "purple",
        "hover:text-pink": hoverColor === "pink",
        "hover:text-blue": hoverColor === "blue",
        "hover:text-red": hoverColor === "red",
        "hover:text-success": hoverColor === "success",
        "hover:text-warning": hoverColor === "warning",
        "hover:text-neutral": hoverColor === "neutral",
        "hover:text-black": hoverColor === "black",
        "hover:text-white": hoverColor === "white",
        "hover:text-milk": hoverColor === "milk",
      })}
      href={href}
      rel={rel}
      target={target}
    >
      {children}
    </a>
  );
};
