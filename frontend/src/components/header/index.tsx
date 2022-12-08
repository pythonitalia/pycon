/** @jsxRuntime classic */

/** @jsx jsx */
import { NavBar } from "@python-italia/pycon-styleguide";
import { jsx } from "theme-ui";

import { useRouter } from "next/router";

import { useLoginState } from "~/components/profile/hooks";
import { getTranslatedMessage } from "~/helpers/use-translated-message";
import { useCurrentLanguage } from "~/locale/context";
import { useHeaderQuery } from "~/types";

import { createHref } from "../link";
import { Logo, MobileLogo } from "../logo";

export const Header = () => {
  const [loggedIn] = useLoginState();
  const language = useCurrentLanguage();
  const router = useRouter();
  const { data } = useHeaderQuery({
    variables: {
      code: process.env.conferenceCode!,
    },
  });
  const { route, query } = useRouter();

  const actions = [
    {
      text: getTranslatedMessage("header.tickets", language),
      icon: "tickets",
      link: "/tickets",
    },
    {
      text:
        router.isReady && loggedIn
          ? getTranslatedMessage("header.dashboard", language)
          : getTranslatedMessage("header.login", language),
      icon: "user",
      link: loggedIn ? "/profile" : "/login",
    },
  ];

  const {
    conference: {
      conferenceMenuEn,
      programMenuEn,
      conferenceMenuIt,
      programMenuIt,
    },
  } = data;

  const conferenceMenu =
    language === "it" ? conferenceMenuIt : conferenceMenuEn;
  const programMenu = language === "it" ? programMenuIt : programMenuEn;

  const mainLinks = conferenceMenu.links;
  const secondaryLinks = programMenu.links;

  const languageSwitchHref = createHref({
    path: route,
    params: query,
    locale: language === "it" ? "en" : "it",
    external: false,
  });

  return (
    <NavBar
      mainLinks={mainLinks}
      secondaryLinks={secondaryLinks}
      actions={actions}
      logo={Logo}
      mobileLogo={MobileLogo}
      bottomBarLink={{
        text: getTranslatedMessage("header.switchLanguage", language),
        link: languageSwitchHref,
      }}
    />
  );
};
