import { Footer as FooterStyleguide } from "@python-italia/pycon-styleguide";
import React from "react";

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

  const language = useCurrentLanguage();
  const menu = language === "en" ? footerEn : footerIt;

  return (
    <FooterStyleguide
      logo={FooterLogo}
      bottomLinks={menu.links}
      socials={[
        { icon: "twitter", link: "https://twitter.com/pyconit" },
        { icon: "facebook", link: "https://www.facebook.com/pythonitalia" },
        { icon: "instagram", link: "https://www.instagram.com/python.it" },
        {
          icon: "linkedin",
          link: "https://www.linkedin.com/company/pycon-italia",
        },
        { icon: "mastodon", link: "https://social.python.it/@pycon" },
      ]}
    />
  );
};
