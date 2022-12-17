import React from "react";

type Props = React.PropsWithChildren<{
  href: string;
  rel?: string;
  target?: string;
}>;

export const Link = ({ href, children, rel, target }: Props) => {
  return (
    <a
      className="text-black hover:text-cream hover:fill-current transition-colors"
      href={href}
      rel={rel}
      target={target}
    >
      {children}
    </a>
  );
};
