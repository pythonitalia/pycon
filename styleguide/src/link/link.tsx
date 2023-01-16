import clsx from "clsx";
import React from "react";
import { Color } from "../types";

type Props = React.PropsWithChildren<{
  href: string;
  rel?: string;
  target?: string;
  hoverColor?: Color;
  noHover?: boolean;
  noLayout?: boolean;
  onClick?: (e: React.MouseEvent<HTMLAnchorElement, MouseEvent>) => void;
}>;

export const Link = ({
  href,
  children,
  rel,
  target,
  hoverColor = "green",
  noHover = false,
  noLayout = false,
  onClick,
}: Props) => {
  return (
    <a
      onClick={onClick}
      className={clsx("text-black transition-colors", {
        "hover:fill-current hover:text-coral":
          hoverColor === "coral" && !noHover,
        "hover:fill-current hover:text-caramel":
          hoverColor === "caramel" && !noHover,
        "hover:fill-current hover:text-cream":
          hoverColor === "cream" && !noHover,
        "hover:fill-current hover:text-yellow":
          hoverColor === "yellow" && !noHover,
        "hover:fill-current hover:text-green":
          hoverColor === "green" && !noHover,
        "hover:fill-current hover:text-purple":
          hoverColor === "purple" && !noHover,
        "hover:fill-current hover:text-pink": hoverColor === "pink" && !noHover,
        "hover:fill-current hover:text-blue": hoverColor === "blue" && !noHover,
        "hover:fill-current hover:text-red": hoverColor === "red" && !noHover,
        "hover:fill-current hover:text-success":
          hoverColor === "success" && !noHover,
        "hover:fill-current hover:text-warning":
          hoverColor === "warning" && !noHover,
        "hover:fill-current hover:text-neutral":
          hoverColor === "neutral" && !noHover,
        "hover:fill-current hover:text-black":
          hoverColor === "black" && !noHover,
        "hover:fill-current hover:text-white":
          hoverColor === "white" && !noHover,
        "hover:fill-current hover:text-milk": hoverColor === "milk" && !noHover,

        contents: noLayout,
      })}
      href={href}
      rel={rel}
      target={target}
    >
      {children}
    </a>
  );
};
