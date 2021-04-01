import clsx from "clsx";
import React, { ReactNode, SVGProps } from "react";
import { FacebookIcon } from "../icons/facebook";
import { InstagramIcon } from "../icons/instagram";
import { TwitterIcon } from "../icons/twitter";
import { Logo } from "../logo/logo";

const SocialLink = ({
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

export const Footer = () => (
  <div className="bg-black">
    <footer className="py-16 px-8 flex justify-between max-w-7xl mx-auto">
      <Logo />

      <nav className="flex space-x-4">
        <li>
          <SocialLink
            href="https://twitter.com/pyconit"
            className="bg-blue-400"
            icon={TwitterIcon}
          >
            Twitter
          </SocialLink>
        </li>
        <li>
          <SocialLink
            href="https://www.facebook.com/pythonitalia/"
            className="bg-blue-700"
            icon={FacebookIcon}
          >
            Facebook
          </SocialLink>
        </li>
        <li>
          <SocialLink
            href="https://www.instagram.com/python.it/"
            className="bg-purple-800"
            icon={InstagramIcon}
          >
            Instagram
          </SocialLink>
        </li>
      </nav>
    </footer>
  </div>
);
