/** @jsxRuntime classic */

/** @jsx jsx */
import { NavBar } from "@python-italia/pycon-styleguide";
import { Action } from "@python-italia/pycon-styleguide/dist/navbar/types";
import { useEffect, useState } from "react";
import { jsx } from "theme-ui";

import { useRouter } from "next/router";

import { useLoginState } from "~/components/profile/hooks";
import { getTranslatedMessage } from "~/helpers/use-translated-message";
import { useCurrentLanguage } from "~/locale/context";
import { useHeaderQuery } from "~/types";

import { createHref } from "../link";
import { Logo, MobileLogo } from "../logo";

export const Header = () => {
  const [isReady, setIsReady] = useState(false);
  const [loggedIn] = useLoginState();
  const language = useCurrentLanguage();
  const { data } = useHeaderQuery({
    variables: {
      code: process.env.conferenceCode!,
    },
  });
  const { route, query } = useRouter();

  useEffect(() => {
    setIsReady(true);
  }, []);

  const {
    conference: {
      conferenceMenuEn,
      programMenuEn,
      conferenceMenuIt,
      programMenuIt,
      isRunning,
      currentDay,
    },
  } = data || { conference: {} };
  const hasSomethingLive = currentDay?.rooms?.some(
    (room) => !!room.streamingUrl,
  );

  const actions: Action[] = [
    isRunning && hasSomethingLive
      ? {
          text: getTranslatedMessage("header.streaming", language),
          icon: "live-circle",
          link: "/streaming",
          background: "red",
          hoverBackground: "red",
        }
      : {
          text: getTranslatedMessage("header.tickets", language),
          icon: "tickets",
          link: "/tickets",
        },
    // {
    //   text:
    //     isReady && loggedIn
    //       ? getTranslatedMessage("header.dashboard", language)
    //       : getTranslatedMessage("header.login", language),
    //   icon: "user",
    //   link: isReady && loggedIn ? "/profile" : "/login",
    // },
  ];

  const conferenceMenu =
    language === "it" ? conferenceMenuIt : conferenceMenuEn;
  const programMenu = language === "it" ? programMenuIt : programMenuEn;

  const mainLinks = conferenceMenu?.links ?? [];
  const secondaryLinks = programMenu?.links ?? [];

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
