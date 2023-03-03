import {
  CardPart,
  Grid,
  Heading,
  Link,
  MultiplePartsCard,
  Page,
  Section,
} from "@python-italia/pycon-styleguide";
import { Icon } from "@python-italia/pycon-styleguide/dist/icons/types";
import { Color } from "@python-italia/pycon-styleguide/dist/types";
import React, { useEffect } from "react";
import { FormattedMessage } from "react-intl";

import Router from "next/router";

import { useCurrentLanguage } from "~/locale/context";
import { useMyProfileQuery } from "~/types";

import { createHref } from "../link";
import { useLoginState } from "../profile/hooks";

type Action = {
  link: string;
  label: React.ReactNode;
  icon?: Icon;
  iconBackground?: Color;
  rightSideIconBackground?: Color;
  rightSideIcon?: Icon;
};

export const ProfilePageHandler = () => {
  const [loggedIn, setLoginState] = useLoginState();
  const language = useCurrentLanguage();

  const { error, data: profileData } = useMyProfileQuery();

  useEffect(() => {
    const loginUrl = `/login`;

    if (error) {
      setLoginState(false);

      Router.push("/login", loginUrl);
    }
  }, [error]);

  useEffect(() => {
    if (!loggedIn) {
      const loginUrl = `/login`;
      setLoginState(false);
      Router.push("/login", loginUrl);
    }
  }, []);

  const { name } = profileData.me;

  const availableActions: Action[] = [
    {
      link: createHref({
        path: "/profile/edit",
        locale: language,
      }),
      label: <FormattedMessage id="profile.myProfile" />,
      icon: "user",
      iconBackground: "blue",
    },
    {
      link: createHref({
        path: "/profile/my-tickets",
        locale: language,
      }),
      label: <FormattedMessage id="profile.myTickets" />,
      icon: "tickets",
      iconBackground: "pink",
    },
    {
      link: createHref({
        path: "/profile/my-proposals",
        locale: language,
      }),
      label: <FormattedMessage id="profile.myProposals" />,
      icon: "email",
      iconBackground: "green",
    },
    {
      link: createHref({
        path: "/profile/my-orders",
        locale: language,
      }),
      label: <FormattedMessage id="profile.myOrders" />,
      icon: "circle",
      iconBackground: "purple",
    },
    {
      link: "",
      label: <FormattedMessage id="profile.logout" />,
      rightSideIcon: "sign-out",
      rightSideIconBackground: "milk",
    },
  ];

  return (
    <Page endSeparator={false}>
      <Section background="coral">
        <Heading size="display2">
          <FormattedMessage
            id="profile.welcome"
            values={{
              name,
            }}
          />
        </Heading>
      </Section>
      <Section>
        <Grid cols={2}>
          {availableActions.map((action) => (
            <Link key={action.link} hoverColor="black" href={action.link}>
              <MultiplePartsCard>
                <CardPart
                  background={action.rightSideIconBackground ?? "cream"}
                  icon={action.icon}
                  iconBackground={action.iconBackground}
                  rightSideIcon={action.rightSideIcon ?? "arrow"}
                  rightSideIconBackground={
                    action.rightSideIconBackground ?? "none"
                  }
                >
                  <Heading size={3}>{action.label}</Heading>
                </CardPart>
              </MultiplePartsCard>
            </Link>
          ))}
        </Grid>
      </Section>
    </Page>
  );
};
