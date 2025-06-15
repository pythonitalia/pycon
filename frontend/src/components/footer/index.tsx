import {
  Footer as FooterStyleguide,
  Heading,
  Text,
} from "@python-italia/pycon-styleguide";
import React, { useState } from "react";
import { FormattedMessage } from "react-intl";

import { useRouter } from "next/router";

import { useCurrentLanguage } from "~/locale/context";
import { useFooterQuery } from "~/types";

import { FooterLogo } from "../icons/footer-logo";
import { useSetCurrentModal } from "../modal/context";

export const Footer = () => {
  const setModal = useSetCurrentModal();
  const { data } = useFooterQuery({
    variables: {
      code: process.env.conferenceCode,
    },
  });
  const { pathname } = useRouter();

  const language = useCurrentLanguage();

  const openNewsletter = () => {
    setModal("newsletter");
  };

  const {
    conference: { footerEn, footerIt },
  } = data || {
    conference: {
      footerEn: { links: [] },
      footerIt: { links: [] },
    },
  };

  const menu: {
    links: {
      text: string;
      link: string;
    }[];
  } = language === "en" ? footerEn : footerIt;

  return (
    <>
      <FooterStyleguide
        logo={FooterLogo}
        bottomLinks={menu.links}
        noTopSpace={pathname === "/"}
        socialsBarLeft={
          <div className="flex flex-col md:flex-row md:items-center gap-6">
            <Heading size={2}>
              <FormattedMessage id="footer.stayTuned" />
            </Heading>
            <div
              className="cursor-pointer hover:text-cream transition-colors"
              onClick={openNewsletter}
            >
              <Text
                size={1}
                decoration="underline"
                weight="strong"
                color="none"
              >
                <FormattedMessage id="footer.subscribeToNewsletter" />
              </Text>
            </div>
          </div>
        }
        socials={[
          {
            icon: "mastodon",
            link: "https://social.python.it/@pycon",
            rel: "me",
          },
          {
            icon: "facebook",
            link: "https://www.facebook.com/pythonitalia",
            rel: "me",
          },
          {
            icon: "instagram",
            link: "https://www.instagram.com/pycon.it",
            rel: "me",
          },
          {
            icon: "linkedin",
            link: "https://www.linkedin.com/company/pycon-italia",
            rel: "me",
          },
          { icon: "twitter", link: "https://twitter.com/pyconit", rel: "me" },
        ]}
      />
    </>
  );
};
