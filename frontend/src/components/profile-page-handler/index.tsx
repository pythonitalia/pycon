import {
  BasicButton,
  Button,
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
import React, { useEffect, useState } from "react";
import { FormattedMessage } from "react-intl";

import Router from "next/router";

import { useCurrentLanguage } from "~/locale/context";
import { useLogoutMutation, useMyProfileQuery } from "~/types";

import { createHref } from "../link";
import { MetaTags } from "../meta-tags";
import { Modal } from "../modal";
import { useLoginState } from "../profile/hooks";

type Action = {
  id: string;
  link?: string;
  onClick?: () => void;
  label: React.ReactNode;
  icon?: Icon;
  iconBackground?: Color;
  rightSideIconBackground?: Color;
  rightSideIcon?: Icon;
};

export const ProfilePageHandler = () => {
  const [showLogoutModal, openLogoutModal] = useState(false);
  const [logout, { loading: isLoggingOut }] = useLogoutMutation();
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

  const onLogout = async () => {
    await logout();
    setLoginState(false);
    window.location.href = `/${language}`;
  };

  const availableActions: Action[] = [
    {
      id: "profile",
      link: createHref({
        path: "/profile/edit",
        locale: language,
      }),
      label: <FormattedMessage id="profile.myProfile" />,
      icon: "user",
      iconBackground: "blue",
    },
    {
      id: "tickets",
      link: createHref({
        path: "/profile/my-tickets",
        locale: language,
      }),
      label: <FormattedMessage id="profile.myTickets" />,
      icon: "tickets",
      iconBackground: "pink",
    },
    {
      id: "proposals",
      link: createHref({
        path: "/profile/my-proposals",
        locale: language,
      }),
      label: <FormattedMessage id="profile.myProposals" />,
      icon: "email",
      iconBackground: "green",
    },
    {
      id: "orders",
      link: createHref({
        path: "/profile/my-orders",
        locale: language,
      }),
      label: <FormattedMessage id="profile.myOrders" />,
      icon: "circle",
      iconBackground: "purple",
    },
    {
      id: "logout",
      link: undefined,
      onClick: () => openLogoutModal(true),
      label: <FormattedMessage id="profile.logout" />,
      rightSideIcon: "sign-out",
      rightSideIconBackground: "milk",
    },
  ];

  return (
    <Page endSeparator={false}>
      <FormattedMessage id="profile.dashboard.title">
        {(text) => <MetaTags title={text} />}
      </FormattedMessage>
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
            <Link
              key={action.id}
              hoverColor="black"
              href={action.link}
              onClick={action.onClick}
              className="cursor-pointer"
            >
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

      <Modal
        title={<FormattedMessage id="profile.logout.title" />}
        onClose={() => openLogoutModal(false)}
        show={showLogoutModal}
        actions={
          <div className="flex flex-col md:flex-row gap-6 justify-end items-center">
            <BasicButton onClick={() => openLogoutModal(false)}>
              <FormattedMessage id="profile.tickets.cancel" />
            </BasicButton>
            <Button
              disabled={isLoggingOut}
              role="alert"
              onClick={onLogout}
              size="small"
            >
              <FormattedMessage id="profile.logout" />
            </Button>
          </div>
        }
      >
        <Heading size={4}>
          <FormattedMessage
            id="profile.logout.body"
            values={{
              name,
            }}
          />
        </Heading>
      </Modal>
    </Page>
  );
};
