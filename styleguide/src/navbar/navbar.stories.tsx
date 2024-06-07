import React from "react";
import { Logo } from "../logo/logo";
import { NavBar } from "./navbar";

export const Standard = ({
  withMainLinks,
  withSecondaryLinks,
  withBottomBarLink,
  withActions,
  ...props
}) => (
  <NavBar
    actions={
      withActions
        ? [
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
          ]
        : []
    }
    mainLinks={
      withMainLinks
        ? [
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
          ]
        : []
    }
    secondaryLinks={
      withSecondaryLinks
        ? new Array(15)
            .fill({
              text: "Beginners Day",
              link: "/beginners-day",
            })
            .map((l, index) => ({
              ...l,
              text: `${l.text} ${index}`,
            }))
        : []
    }
    logo={Logo}
    mobileLogo={Logo}
    bottomBarLink={
      withBottomBarLink
        ? {
            link: "/it",
            text: "Switch to Italian",
          }
        : undefined
    }
    {...props}
  />
);

export default {
  title: "NavBar",
  component: Standard,
  argTypes: {
    withMainLinks: {
      defaultValue: true,
      control: {
        type: "boolean",
      },
    },
    withSecondaryLinks: {
      defaultValue: true,
      control: {
        type: "boolean",
      },
    },
    withBottomBarLink: {
      defaultValue: true,
      control: {
        type: "boolean",
      },
    },
    withActions: {
      defaultValue: true,
      control: {
        type: "boolean",
      },
    },
  },
};
