import clsx from "clsx";
import React from "react";
import { useToggle } from "react-use";
import { FacebookIcon } from "../icons/facebook";
import { InstagramIcon } from "../icons/instagram";
import { TwitterIcon } from "../icons/twitter";
import { Logo } from "../logo/logo";
import { MenuButton } from "../menu-button/menu-button";
import { SocialLink } from "../social-link/social-link";
import { Color } from "../types";

type Link = {
  href: string;
  title: string;
};

const MenuLinks = ({ links }: { links: Link[] }) => (
  <nav className="list-none space-y-8">
    {links.map((link) => (
      <li>
        <a href={link.href} className="text-white text-4xl hover:underline">
          {link.title}
        </a>
      </li>
    ))}
  </nav>
);

const Menu = ({ links }: { links: Link[] }) => {
  const linksA = links.filter((_, index) => index % 2 === 0);
  const linksB = links.filter((_, index) => index % 2 !== 0);

  return (
    <div className="p-12 py-12 sm:p-16 justify-between max-w-7xl mx-auto gap-8 grid sm:grid-cols-2 md:grid-cols-4">
      <MenuLinks links={linksA} />
      <MenuLinks links={linksB} />

      <div className="space-y-4">
        <h2 className="text-xl font-bold uppercase">Contact</h2>

        <p>
          Enquiries
          <br />{" "}
          <a href="mailto:info@pycon.it" className="text-white underline">
            info@pycon.it
          </a>
        </p>
      </div>

      <div className="space-y-4">
        <h2 className="uppercase font-bold text-xl">Follow us</h2>

        <nav className="flex space-x-4 list-none">
          <li>
            <SocialLink
              href="https://twitter.com/pyconit"
              className="bg-keppel border-black border-4 fill-current text-black"
              icon={TwitterIcon}
            >
              Twitter
            </SocialLink>
          </li>
          <li>
            <SocialLink
              href="https://www.facebook.com/pythonitalia/"
              className="bg-purple border-black border-4 fill-current text-black"
              icon={FacebookIcon}
            >
              Facebook
            </SocialLink>
          </li>
          <li>
            <SocialLink
              href="https://www.instagram.com/python.it/"
              className="bg-orange border-black border-4 fill-current text-black"
              icon={InstagramIcon}
            >
              Instagram
            </SocialLink>
          </li>
        </nav>
      </div>
    </div>
  );
};


export const Header = ({
  links = [],
  backgroundColor = "white",
}: {
  links?: Link[];
  backgroundColor?: Color;
}) => {
  const [menuOpen, toggleMenuOpen] = useToggle(false);

  return (
    <div
      className={clsx({
        [`bg-${backgroundColor}`]: !menuOpen,
        "bg-orange": menuOpen,
      })}
    >
      <header className="p-8 flex justify-between max-w-7xl mx-auto">
        <a href="/">
          <Logo className="w-40" />
        </a>

        <MenuButton onClick={toggleMenuOpen} />
      </header>

      {menuOpen ? (
        <div className="bg-orange border-t-4 border-b-4 border-black absolute z-20 w-full">
          <Menu links={links} />
        </div>
      ) : null}
    </div>
  );
};
