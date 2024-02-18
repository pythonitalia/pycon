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

  const { error, data: profileData } = useMyProfileQuery({
    variables: {
      conferenceCode: process.env.conferenceCode,
    },
  });

  useEffect(() => {
    const loginUrl = "/login";

    if (error) {
      setLoginState(false);

      Router.push("/login", loginUrl);
    }
  }, [error]);

  useEffect(() => {
    if (!loggedIn) {
      const loginUrl = "/login";
      setLoginState(false);
      Router.push("/login", loginUrl);
    }
  }, []);

  const { name, fullName } = profileData.me;

  const onLogout = async () => {
    await logout();
    setLoginState(false);
    window.location.href = `/${language}`;
  };

  const isStaffOrSponsor = profileData.me.conferenceRoles.some((role) =>
    ["STAFF", "SPONSOR"].indexOf(role),
  );

  const availableActions = [
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
    isStaffOrSponsor
      ? {
          id: "sponsors",
          link: createHref({
            path: "/profile/sponsor",
            locale: language,
          }),
          label: <FormattedMessage id="profile.sponsorSection" />,
          icon: "web",
          iconBackground: "purple",
        }
      : null,
    {
      id: "logout",
      link: undefined,
      onClick: () => openLogoutModal(true),
      label: <FormattedMessage id="profile.logout" />,
      rightSideIcon: "sign-out",
      rightSideIconBackground: "milk",
    },
  ].filter((action) => action !== null) as Action[];

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
              name: name || fullName,
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
          <div className="flex flex-col-reverse md:flex-row gap-6 justify-end items-center">
            <BasicButton onClick={() => openLogoutModal(false)}>
              <FormattedMessage id="profile.tickets.cancel" />
            </BasicButton>
            <Button
              disabled={isLoggingOut}
              variant="alert"
              onClick={onLogout}
              size="small"
              fullWidth="mobile"
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
              name: name || fullName,
            }}
          />
        </Heading>
      </Modal>
    </Page>
  );
};
