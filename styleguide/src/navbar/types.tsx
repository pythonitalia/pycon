export type Action = {
  icon: string;
  text?: string;
  link?: string;
  onClick?: () => void;
};

export type Link = {
  text: string;
  link: string;
};
