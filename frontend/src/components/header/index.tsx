/** @jsxRuntime classic */
/** @jsx jsx */
import dynamic from "next/dynamic";
import { useRouter } from "next/router";
import { Fragment, useEffect, useRef } from "react";
import { FormattedMessage } from "react-intl";
import { Box, Flex, Grid, Heading, jsx } from "theme-ui";
import useOnClickOutside from "use-onclickoutside";

import { useLoginState } from "~/components/profile/hooks";
import { useToggle } from "~/helpers/use-toggle";
import { useAlternateLinks, useCurrentLanguage } from "~/locale/context";
import { useHeaderQuery } from "~/types";

import { Button } from "../button/button";
import { EnglishIcon } from "../icons/english";
import { ItalianIcon } from "../icons/italian";
import { Link } from "../link";
import { Logo } from "../logo";
import { SocialLinks } from "../social-links";
import { SnakeBurger } from "./snake-burger";

const ProfileLink = dynamic(
  () => import("./profile-link").then((mod) => mod.ProfileLink),
  { ssr: false },
);

const LanguagePicker: React.SFC<{ language: string }> = ({
  language,
  ...props
}) => {
  const alternateLinks = useAlternateLinks();

  return (
    <Flex sx={{ alignItems: "center", height: 50, mt: "-4px" }} {...props}>
      <Link path={alternateLinks.en} sx={{ height: 40 }}>
        <EnglishIcon active={language === "en"} sx={{ width: 40, mr: 2 }} />
      </Link>
      <Link path={alternateLinks.it} sx={{ height: 40 }}>
        <ItalianIcon active={language === "it"} sx={{ width: 40, mr: 4 }} />
      </Link>
    </Flex>
  );
};

const Links: React.SFC<{
  links: { href: string; title: string; page?: { slug: string } | null }[];
}> = ({ links }) => (
  <Fragment>
    {links.map((link) => {
      let path = link.page ? "/[lang]/[slug]" : link.href;

      // nasty hack to make client side routing work with next.js
      path = path.replace("/en", "/[lang]").replace("/it", "/[lang]");

      return (
        <Link variant="header" path={path} key={link.href} params={link.page}>
          {link.title}
        </Link>
      );
    })}
  </Fragment>
);

const WARNING_MESSAGE_HEIGHT = [80, 80, 60];

export const Header = () => {
  const language = useCurrentLanguage();
  const router = useRouter();
  const { loading, data } = useHeaderQuery({
    variables: {
      code: process.env.conferenceCode!,
      language,
    },
  });

  const [loggedIn] = useLoginState();
  const [open, toggleOpen, _, close] = useToggle(false);
  const headerRef = useRef(null);

  useOnClickOutside(headerRef, close);
  useEffect(close, [router.asPath]);

  if (loading || !data) {
    return null;
  }

  const {
    conference: { conferenceMenu, programMenu },
  } = data;

  return (
    <Fragment>
      <Box
        sx={
          {
            height: WARNING_MESSAGE_HEIGHT,
            backgroundColor: "black",
            color: "white",
            position: open ? "fixed" : "relative",
            width: "100%",
            zIndex: "header",
          } as any
        }
      >
        <Box
          sx={{
            width: "100%",
            maxWidth: "largeContainer",
            mx: "auto",
            px: 2,
            display: "flex",
            alignItems: "center",
            height: "100%",
          }}
        >
          <Link
            sx={{ color: "white", textUnderlineOffset: 4 }}
            path="/[lang]/blog/[slug]"
            params={{ slug: "pycon-11-cancelled" }}
          >
            <FormattedMessage id="header.coronaVirus" />
          </Link>
        </Box>
      </Box>

      <Box
        ref={headerRef}
        sx={
          {
            top: WARNING_MESSAGE_HEIGHT,
            left: 0,
            pt: 3,
            width: "100%",
            height: open ? "100%" : "",
            zIndex: "header",
            position: open ? "fixed" : "absolute",
            borderBottom: open ? "primary" : "",
            backgroundColor: open ? "orange" : "",
            overflowY: open ? "scroll" : "initial",
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
          <Link path="/[lang]">
            <Logo
              sx={{
                width: ["166px", null, "250px"],
                height: "auto",
              }}
            />
          </Link>

          <Flex
            sx={{
              alignItems: "center",
            }}
          >
            <LanguagePicker
              language={language}
              sx={{
                display: ["none", "block"],
              }}
            />

            <ProfileLink />

            <Button
              sx={{
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                justifyContent: "center",

                mt: "-5px",

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
                path={loggedIn ? "/[lang]/profile" : "/[lang]/login"}
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
