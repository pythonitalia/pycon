import { NavBar } from "@python-italia/pycon-styleguide";
import type { Action } from "@python-italia/pycon-styleguide/dist/navbar/types";
import React, { useEffect, useState } from "react";

import { useLoginState } from "~/components/profile/hooks";
import { getTranslatedMessage } from "~/helpers/use-translated-message";
import { useHeaderQuery } from "~/types";

import { Logo, MobileLogo } from "../logo";

export const Header = () => {
  const [isReady, setIsReady] = useState(false);
  const [loggedIn] = useLoginState();
  const { data } = useHeaderQuery({
    variables: {
      code: process.env.conferenceCode!,
    },
  });

  useEffect(() => {
    setIsReady(true);
  }, []);

  const {
    conference: { conferenceMenu, programMenu, isRunning, currentDay },
  } = data || { conference: {} };
  // const hasSomethingLive = currentDay?.rooms?.some(
  //   (room) => !!room.streamingUrl,
  // );

  const actions: Action[] = [
    isRunning
      ? {
          text: getTranslatedMessage("header.streaming"),
          icon: "live-circle",
          link: "/streaming",
          background: "red",
          hoverBackground: "red",
        }
      : {
          text: getTranslatedMessage("header.tickets"),
          icon: "tickets",
          link: "/tickets",
        },
    {
      text:
        isReady && loggedIn
          ? getTranslatedMessage("header.dashboard")
          : getTranslatedMessage("header.login"),
      icon: "user",
      link: isReady && loggedIn ? "/profile" : "/login",
    },
  ];

  const mainLinks = conferenceMenu?.links ?? [];
  const secondaryLinks = programMenu?.links ?? [];

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
