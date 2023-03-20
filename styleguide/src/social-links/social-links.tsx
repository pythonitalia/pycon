import React from "react";
import { Color } from "../types";
import { SocialLink, SocialLinkProps } from "./social-link";

type Props = {
  socials: SocialLinkProps[];
  color?: Color;
  hoverColor?: Color;
};

export const SocialLinks = ({
  socials,
  color = "black",
  hoverColor = "cream",
}: Props) => {
  return (
    <ul className="flex gap-9">
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
