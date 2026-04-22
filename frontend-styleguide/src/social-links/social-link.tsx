import React from "react";
import { getIcon } from "../icons/icons";
import type { Icon } from "../icons/types";
import { Link } from "../link";
import type { Color } from "../types";

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
