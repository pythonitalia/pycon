import { NavBar } from "@python-italia/pycon-styleguide";
import type { Action } from "@python-italia/pycon-styleguide/dist/navbar/types";
import React, { useEffect, useState } from "react";

import { useLoginState } from "~/components/profile/hooks";
import { getTranslatedMessage } from "~/helpers/use-translated-message";
import { useCurrentLanguage } from "~/locale/context";
import { useHeaderQuery } from "~/types";

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

  useEffect(() => {
    setIsReady(true);
  }, []);

  const {
    conference: { conferenceMenuEn, programMenuEn, isRunning },
  } = data || { conference: {} };

  const actions: Action[] = [
    isRunning
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
    {
      text:
        isReady && loggedIn
          ? getTranslatedMessage("header.dashboard", language)
          : getTranslatedMessage("header.login", language),
      icon: "user",
      link: isReady && loggedIn ? "/profile" : "/login",
    },
  ];

  const mainLinks = conferenceMenuEn?.links ?? [];
  const secondaryLinks = programMenuEn?.links ?? [];

  return (
    <header>
      <NavBar
        mainLinks={mainLinks}
        secondaryLinks={secondaryLinks}
        actions={actions}
        logo={Logo}
        mobileLogo={MobileLogo}
      />
    </header>
  );
};
