/** @jsx jsx */

import { Box, Button, Flex, Grid, Heading } from "@theme-ui/components";
import { graphql, useStaticQuery } from "gatsby";
import { jsx } from "theme-ui";

import { HeaderQuery } from "../../generated/graphql";
import { useToggle } from "../../helpers/use-toggle";
import { Link } from "../link";
import { Logo } from "../logo";
import { SocialLinks } from "../social-links";
import { SnakeBurger } from "./snake-burger";

export const Header = () => {
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

  const [open, toggleOpen] = useToggle(false);

  return (
    <Box
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
        <Logo
          sx={{
            width: ["37vw", "33vw", "25vw", "18vw"],
            height: "auto",
          }}
        />

        <Flex
          sx={{
            alignItems: ["center", "flex-start"],
          }}
        >
          <Button>Login</Button>
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
              <Heading variant="header">Contact</Heading>

              <dl>
                <dt>Become a sponsor</dt>
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
                <dt>Enquiries</dt>
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
              <Heading variant="header">Follow us</Heading>

              <SocialLinks variant="header" />
            </Box>
          </Grid>
        </Box>
      )}
    </Box>
  );
};
