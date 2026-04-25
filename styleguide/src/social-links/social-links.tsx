import clsx from "clsx";
import React from "react";
import { Color } from "../types";
import { SocialLink, SocialLinkProps } from "./social-link";

type Props = {
  socials: SocialLinkProps[];
  color?: Color;
  hoverColor?: Color;
  className?: string;
};

export const SocialLinks = ({
  socials,
  color = "black",
  hoverColor = "cream",
  className,
}: Props) => {
  return (
    <ul className={clsx("flex gap-9", className)}>
      {socials.map((social) => (
        <li
          key={social.icon}
          className="w-6 h-6 flex items-center justify-center"
        >
          <SocialLink hoverColor={hoverColor} color={color} {...social} />
        </li>
      ))}
    </ul>
  );
};
