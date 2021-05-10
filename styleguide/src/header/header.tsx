import clsx from "clsx";
import React from "react";
import { useToggle } from "react-use";
import { FacebookIcon } from "../icons/facebook";
import { InstagramIcon } from "../icons/instagram";
import { TwitterIcon } from "../icons/twitter";
import { Logo } from "../logo/logo";
import { MenuButton } from "../menu-button/menu-button";
import { SocialLink } from "../social-link/social-link";

const Menu = () => (
  <div className="p-12 py-12 sm:p-16 justify-between max-w-7xl mx-auto gap-8 grid sm:grid-cols-2 md:grid-cols-4">
    <nav className="list-none space-y-8">
      <li>
        <a href="/" className="text-white text-4xl hover:underline">
          Home
        </a>
      </li>
      <li>
        <a href="/" className="text-white text-4xl hover:underline">
          Info
        </a>
      </li>
    </nav>
    <nav className="list-none space-y-8">
      <li>
        <a href="/" className="text-white text-4xl hover:underline">
          Home
        </a>
      </li>
      <li>
        <a href="/" className="text-white text-4xl hover:underline">
          Info
        </a>
      </li>
    </nav>

    <div className="space-y-4">
      <h2 className="uppercase font-bold text-xl">Contact</h2>

      <p>
        Become a sponsor
        <br />{" "}
        <a href="mailto:sponsor@pycon.it" className="text-white underline">
          sponsor@pycon.it
        </a>
      </p>

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

export const Header = () => {
  const [menuOpen, toggleMenuOpen] = useToggle(true);

  return (
    <div
      className={clsx({
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
        <div className="bg-orange border-t-4 border-b-4 border-black absolute z-10 w-full">
          <Menu />
        </div>
      ) : null}
    </div>
  );
};
