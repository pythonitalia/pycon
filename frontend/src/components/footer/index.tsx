import { Footer as FooterStyleguide } from "@python-italia/pycon-styleguide";
import React from "react";

import { useRouter } from "next/router";

import { useCurrentLanguage } from "~/locale/context";
import { useFooterQuery } from "~/types";

import { FooterLogo } from "../icons/footer-logo";

export const Footer = () => {
  const {
    data: {
      conference: { footerEn, footerIt },
    },
  } = useFooterQuery({
    variables: {
      code: process.env.conferenceCode,
    },
  });
  const { pathname } = useRouter();

  const language = useCurrentLanguage();
  const menu = language === "en" ? footerEn : footerIt;

  return (
    <FooterStyleguide
      logo={FooterLogo}
      bottomLinks={menu.links}
      noTopSpace={pathname === "/"}
      socials={[
        { icon: "twitter", link: "https://twitter.com/pyconit", rel: "me" },
        {
          icon: "facebook",
          link: "https://www.facebook.com/pythonitalia",
          rel: "me",
        },
        {
          icon: "instagram",
          link: "https://www.instagram.com/python.it",
          rel: "me",
        },
        {
          icon: "linkedin",
          link: "https://www.linkedin.com/company/pycon-italia",
          rel: "me",
        },
        {
          icon: "mastodon",
          link: "https://social.python.it/@pycon",
          rel: "me",
        },
      ]}
    />
  );
};
