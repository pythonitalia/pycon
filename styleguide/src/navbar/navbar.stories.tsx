import React from "react";
import { Logo } from "../logo/logo";
import { NavBar } from "./navbar";

export const Standard = (props) => (
  <NavBar
    actions={[
      {
        text: "Buy Tickets",
        icon: "tickets",
        link: "/tickets",
      },
      {
        text: "Dashboard",
        icon: "user",
        background: "error",
        hoverBackground: "error",
      },
    ]}
    mainLinks={[
      {
        text: "Live",
        link: "/live",
      },
      {
        text: "Agenda",
        link: "/schedule",
      },
      {
        text: "Speakers",
        link: "/speakers",
      },
      {
        text: "Where",
        link: "/where",
      },
      {
        text: "Keynotes",
        link: "/keynotes",
      },
      {
        text: "Tickets",
        link: "/tickets",
      },
    ]}
    secondaryLinks={new Array(15)
      .fill({
        text: "Beginners Day",
        link: "/beginners-day",
      })
      .map((l, index) => ({
        ...l,
        text: `${l.text} ${index}`,
      }))}
    logo={Logo}
    mobileLogo={Logo}
    bottomBarLink={{
      link: "/it",
      text: "Switch to Italian",
    }}
    {...props}
  />
);

export default {
  title: "NavBar",
  component: Standard,
  argTypes: {},
};
