/** @jsx jsx */

import { Location } from "@reach/router";
import { Box, Button, Flex, Grid, Heading } from "@theme-ui/components";
import { graphql, useStaticQuery } from "gatsby";
import { useEffect, useRef } from "react";
import { FormattedMessage } from "react-intl";
import { jsx } from "theme-ui";
import useOnClickOutside from "use-onclickoutside";

import { useLoginState } from "../../app/profile/hooks";
import { HeaderQuery } from "../../generated/graphql";
import { useToggle } from "../../helpers/use-toggle";
import { Link } from "../link";
import { Logo } from "../logo";
import { SocialLinks } from "../social-links";
import { SnakeBurger } from "./snake-burger";

export const HeaderContent = ({ location }: { location: any }) => {
  const {
    backend: {
      conference: { conferenceMenu, programMenu },
    },
  } = useStaticQuery<HeaderQuery>(graphql`
    query Header {
      backend {
        conference {
          conferenceMenu: menu(identifier: "conference-nav") {
            links {
              title
              href
            }
          }
          programMenu: menu(identifier: "program-nav") {
            links {
              title
              href
            }
          }
        }
      }
    }
  `);

  const [loggedIn] = useLoginState();
  const [open, toggleOpen, _, close] = useToggle(false);
  const headerRef = useRef(null);

  useEffect(close, [location]);
  useOnClickOutside(headerRef, close);

  return (
    <Box
      ref={headerRef}
      sx={{
        position: "absolute",
        top: 0,
        left: 0,
        pt: 3,
        width: "100%",
        zIndex: "header",
        backgroundColor: open ? "orange" : "",
      }}
    >
      <Flex
        sx={{
          maxWidth: "largeContainer",
          mx: "auto",
          mb: 4,
          px: 2,
          justifyContent: "space-between",
          alignItems: ["center", "flex-start"],
        }}
      >
        <Link href="/:language">
          <Logo
            sx={{
              width: ["37vw", "33vw", "25vw", "18vw"],
              height: "auto",
            }}
          />
        </Link>

        <Flex
          sx={{
            alignItems: ["center", "flex-start"],
          }}
        >
          <Link
            href={loggedIn ? "/:language/profile" : "/:language/login"}
            variant="button"
            sx={{ mr: 5 }}
          >
            {loggedIn && <FormattedMessage id="header.profile" />}
            {!loggedIn && <FormattedMessage id="header.login" />}
          </Link>

          <Button
            sx={{
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              justifyContent: "center",

              px: [1, 3],
              py: [1, 2],
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
            borderBottom: "primary",
          }}
        >
          <Grid
            columns={[1, 2, 4]}
            sx={{
              maxWidth: "container",
              mx: "auto",
              py: 4,
              px: 2,
            }}
          >
            <Box as="nav">
              {conferenceMenu!.links.map(link => (
                <Link variant="header" href={link.href} key={link.href}>
                  {link.title}
                </Link>
              ))}
            </Box>
            <Box as="nav">
              {programMenu!.links.map(link => (
                <Link variant="header" href={link.href} key={link.href}>
                  {link.title}
                </Link>
              ))}
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
                    href="mailto:sponsor@pycon.it"
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
                    href="mailto:info@pycon.it"
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
  );
};

export const Header = () => (
  <Location>{({ location }) => <HeaderContent location={location} />}</Location>
);
