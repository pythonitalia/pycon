import clsx from "clsx";
import React, { ReactNode, SVGProps } from "react";

export const SocialLink = ({
  href,
  className,
  icon,
  children,
}: {
  className: string;
  href: string;
  children: ReactNode;
  icon: (props: SVGProps<SVGSVGElement>) => JSX.Element;
}) => {
  const IconComponent = icon;

  return (
    <a
      href={href}
      className={clsx(
        "w-10 h-10 rounded-full flex items-center justify-center text-white",
        className
      )}
    >
      <IconComponent className="fill-current" />{" "}
      <div className="sr-only">{children}</div>
    </a>
  );
};
