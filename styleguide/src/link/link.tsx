import React from "react";

type Props = React.PropsWithChildren<{
  href: string;
}>;

export const Link = ({ href, children }: Props) => {
  return (
    <a className="text-black hover:text-cream transition-colors" href={href}>
      {children}
    </a>
  );
};
