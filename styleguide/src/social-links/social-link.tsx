import React from "react";
import { Link } from "../link";
import { Color } from "../types";
import { getIcon } from "../icons/icons";
import { Icon } from "../icons/types";

export type SocialLinkProps = {
  link: string;
  icon: Icon;
  rel?: string;
  color?: Color;
  hoverColor?: Color;
};

export const SocialLink = ({
  link,
  icon,
  rel,
  color,
  hoverColor,
}: SocialLinkProps) => {
  const Icon = getIcon(icon);
  return (
    <Link
      color={color}
      hoverColor={hoverColor}
      target="_blank"
      href={link}
      rel={rel}
      className="w-full h-full"
    >
      <Icon className="w-full h-full" />
    </Link>
  );
};
