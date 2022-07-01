/** @jsxRuntime classic */

/** @jsx jsx */
import { Fragment, useEffect, useRef } from "react";
import { FormattedMessage } from "react-intl";
import { Box, Flex, Grid, Heading, jsx } from "theme-ui";
import useOnClickOutside from "use-onclickoutside";

import { useRouter } from "next/router";

import { useLoginState } from "~/components/profile/hooks";
import { useToggle } from "~/helpers/use-toggle";
import { useCurrentLanguage } from "~/locale/context";
import { useHeaderQuery } from "~/types";

import { Button } from "../button/button";
import { EnglishIcon } from "../icons/english";
import { ItalianIcon } from "../icons/italian";
import { Link } from "../link";
import { Logo } from "../logo";
import { SocialLinks } from "../social-links";
import { ProfileLink } from "./profile-link";
import { SnakeBurger } from "./snake-burger";

const LanguagePicker = ({ language, ...props }: { language: string }) => {
  const { route, query } = useRouter();

  return (
    <Flex sx={{ alignItems: "center" }} {...props}>
      <Link
        path={route}
        params={query}
        locale="en"
        sx={{ height: 40, display: "inline-block" }}
      >
        <EnglishIcon active={language === "en"} sx={{ width: 40, mr: 2 }} />
      </Link>
      <Link
        path={route}
        params={query}
        locale="it"
        sx={{ height: 40, display: "inline-block" }}
      >
        <ItalianIcon active={language === "it"} sx={{ width: 40, mr: 4 }} />
      </Link>
    </Flex>
  );
};

const Links = ({
  links,
}: {
  links: { href: string; title: string; page?: { slug: string } | null }[];
}) => (
  <Fragment>
    {links.map((link) => {
      const path = link.href;

      return (
        <Link variant="header" path={path} key={link.href}>
          {link.title}
        </Link>
      );
    })}
  </Fragment>
);

const ScheduleLink = () => {
  return (
    <Link
      variant="button"
      path="/schedule"
      sx={{ mr: 2, background: "orange" }}
    >
      <FormattedMessage id="header.schedule" />
    </Link>
  );
};

export const Header = () => {
  const language = useCurrentLanguage();
  const router = useRouter();
  const { loading, data } = useHeaderQuery({
    variables: {
      code: process.env.conferenceCode!,
    },
  });

  const [loggedIn] = useLoginState();
  const [open, toggleOpen, _, close] = useToggle(false);
  const headerRef = useRef(null);
  const {
    query: { photo, archive },
  } = useRouter();
  const isInPhotoMode = photo == "1";
  const isInArchiveMode = archive == "1";

  useOnClickOutside(headerRef, close);
  useEffect(close, [router.asPath]);

  if (isInPhotoMode) {
    return null;
  }

  if (loading || !data) {
    return null;
  }

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

  return (
    <Fragment>
      <Box
        ref={headerRef}
        sx={
          {
            top: 0,
            left: 0,
            pt: 3,
            width: "100%",
            height: open ? "100%" : "",
            zIndex: "header",
            position: open ? "fixed" : "relative",
            borderBottom: open ? "primary" : "",
            backgroundColor: open ? "orange" : "",
            overflowY: open ? "scroll" : "initial",
            "@media print": {
              display: "none",
            },
          } as any
        }
      >
        <Flex
          sx={{
            maxWidth: "largeContainer",
            mx: "auto",
            mb: 4,
            px: 2,
            justifyContent: "space-between",
            alignItems: "flex-start",
          }}
        >
          <Link path="/">
            <Logo
              sx={{
                width: ["166px", null, "250px"],
                height: "auto",
              }}
            />
          </Link>

          <Flex
            sx={{
              alignItems: ["flex-start", "center"],
            }}
          >
            <Box
              sx={{
                display: "flex",
                alignItems: "center",
              }}
            >
              <LanguagePicker
                language={language}
                sx={{
                  display: ["none", "block"],
                }}
              />
              <ScheduleLink />
              {!isInArchiveMode && <ProfileLink />}
            </Box>

            <Button
              sx={{
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                justifyContent: "center",

                px: 3,
                py: 2,

                cursor: "pointer",
              }}
              onClick={toggleOpen}
              variant="white"
            >
              <SnakeBurger />
              {open ? "Close" : "Menu"}
            </Button>
          </Flex>
        </Flex>

        {open && (
          <Box
            sx={{
              borderTop: "primary",
            }}
          >
            <Grid
              columns={[1, 2, 4]}
              sx={{
                maxWidth: "container",
                mx: "auto",
                py: 4,
                px: 3,
              }}
            >
              <LanguagePicker
                language={language}
                sx={{
                  display: ["block", "none"],
                }}
              />

              <Link
                path={loggedIn ? "/profile" : "/login"}
                variant="header"
                sx={{ mr: 5, display: ["block", "none"] }}
              >
                {loggedIn && <FormattedMessage id="header.profile" />}
                {!loggedIn && <FormattedMessage id="header.login" />}
              </Link>

              <Box as="nav">
                <Links links={conferenceMenu!.links} />
              </Box>
              <Box as="nav">
                <Links links={programMenu!.links} />
              </Box>
              <Box>
                <Heading variant="header">
                  <FormattedMessage id="header.contact" />
                </Heading>

                <dl>
                  <dt>
                    <FormattedMessage id="header.becomeASponsor" />
                  </dt>
                  <Box as="dd" sx={{ mb: 3 }}>
                    <Link
                      sx={{
                        color: "white",
                      }}
                      path="mailto:sponsor@pycon.it"
                    >
                      sponsor@pycon.it
                    </Link>
                  </Box>
                  <dt>
                    <FormattedMessage id="header.enquiries" />
                  </dt>
                  <Box as="dd" sx={{ mb: 3 }}>
                    <Link
                      sx={{
                        color: "white",
                      }}
                      path="mailto:info@pycon.it"
                    >
                      info@pycon.it
                    </Link>
                  </Box>
                </dl>
              </Box>
              <Box>
                <Heading variant="header">
                  <FormattedMessage id="header.followus" />
                </Heading>

                <SocialLinks variant="header" />
              </Box>
            </Grid>
          </Box>
        )}
      </Box>
    </Fragment>
  );
};
