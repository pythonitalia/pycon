import { Icon } from "../icons/types";

export type Action = {
  icon: Icon;
  text?: string;
  link?: string;
  onClick?: () => void;
};

export type Link = {
  text: string;
  link: string;
};
