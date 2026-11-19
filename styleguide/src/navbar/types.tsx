import { Icon } from "../icons/types";
import { Color } from "../types";

export type Action = {
  icon: Icon;
  background?: Color;
  hoverBackground?: Color;
  text?: string;
  link?: string;
  onClick?: () => void;
};

export type Link = {
  text: string;
  link: string;
};
