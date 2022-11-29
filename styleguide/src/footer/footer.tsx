import React from "react";
import { FacebookIcon } from "../icons/facebook";
import { InstagramIcon } from "../icons/instagram";
import { TwitterIcon } from "../icons/twitter";
import { Logo } from "../logo/logo";
import { SocialLink } from "../social-link/social-link";

export const Footer = () => (
  <div className="bg-black">
    <footer className="py-16 px-8 md:flex justify-between max-w-7xl mx-auto space-y-8">
      <Logo className="mx-auto w-full max-w-[13rem] md:w-40 md:m-0" />

      <nav className="flex space-x-4 justify-center list-none">
        <li>
          <SocialLink
            href="https://twitter.com/pyconit"
            className="bg-green"
            icon={TwitterIcon}
          >
            Twitter
          </SocialLink>
        </li>
        <li>
          <SocialLink
            href="https://www.facebook.com/pythonitalia/"
            className="bg-purple"
            icon={FacebookIcon}
          >
            Facebook
          </SocialLink>
        </li>
        <li>
          <SocialLink
            href="https://www.instagram.com/python.it/"
            className="bg-coral"
            icon={InstagramIcon}
          >
            Instagram
          </SocialLink>
        </li>
      </nav>
    </footer>
  </div>
);
