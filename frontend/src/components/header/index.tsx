/** @jsx jsx */

import { Location } from "@reach/router";
import { Box, Button, Flex, Grid, Heading } from "@theme-ui/components";
import { graphql, useStaticQuery } from "gatsby";
import { Fragment, useEffect, useRef } from "react";
import { FormattedMessage } from "react-intl";
import { jsx } from "theme-ui";
import useOnClickOutside from "use-onclickoutside";

import { useLoginState } from "../../app/profile/hooks";
import { useAlternateLinks, useCurrentLanguage } from "../../context/language";
import { HeaderQuery } from "../../generated/graphql";
import { useToggle } from "../../helpers/use-toggle";
import { EnglishIcon } from "../icons/english";
import { ItalianIcon } from "../icons/italian";
import { Link } from "../link";
import { Logo } from "../logo";
import { SocialLinks } from "../social-links";
import { SnakeBurger } from "./snake-burger";

const LanguagePicker: React.SFC<{ language: string }> = ({
  language,
  ...props
}) => {
  const alternateLinks = useAlternateLinks();

  return (
    <Flex sx={{ alignItems: "center", height: 50, mt: "-3px" }} {...props}>
      <Link href={alternateLinks.en} sx={{ height: 40 }}>
        <EnglishIcon active={language === "en"} sx={{ width: 40, mr: 2 }} />
      </Link>
      <Link href={alternateLinks.it} sx={{ height: 40 }}>
        <ItalianIcon active={language === "it"} sx={{ width: 40, mr: 4 }} />
      </Link>
    </Flex>
  );
};

const Links: React.SFC<{
  language: "en" | "it";
  links: { hrefIt: string; hrefEn: string; titleEn: string; titleIt: string }[];
}> = ({ language, links }) => {
  const titleKey = { en: "titleEn", it: "titleIt" }[
    language
  ] as keyof typeof links[0];
  const hrefKey = { en: "hrefEn", it: "hrefIt" }[
    language
  ] as keyof typeof links[0];

  return (
    <Fragment>
      {links.map(link => (
        <Link variant="header" href={link[hrefKey]} key={link[hrefKey]}>
          {link[titleKey]}
        </Link>
      ))}
    </Fragment>
  );
};

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
              titleEn: title(language: "en")
              titleIt: title(language: "it")
              hrefEn: href(language: "en")
              hrefIt: href(language: "it")
            }
          }
          programMenu: menu(identifier: "program-nav") {
            links {
              titleEn: title(language: "en")
              titleIt: title(language: "it")
              hrefEn: href(language: "en")
              hrefIt: href(language: "it")
            }
          }
        }
      }
    }
  `);

  const [loggedIn] = useLoginState();
  const [open, toggleOpen, _, close] = useToggle(false);
  const headerRef = useRef(null);
  const language = useCurrentLanguage();

  useEffect(close, [location]);
  useOnClickOutside(headerRef, close);

  return (
    <Box
      ref={headerRef}
      sx={{
        top: 0,
        left: 0,
        pt: 3,
        width: "100%",
        height: open ? "100%" : "",
        zIndex: "header",
        position: open ? "fixed" : "absolute",
        borderBottom: open ? "primary" : "",
        backgroundColor: open ? "orange" : "",
        overflowX: open ? "scroll" : "",
      }}
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
        <Link href="/:language">
          <Logo
            sx={{
              width: ["166px", null, "250px"],
              height: "auto",
            }}
          />
        </Link>

        <Flex
          sx={{
            alignItems: ["center", "flex-start"],
          }}
        >
          <LanguagePicker
            language={language}
            sx={{
              display: ["none", "block"],
            }}
          />

          <Link
            href={loggedIn ? "/:language/profile" : "/:language/login"}
            variant="button"
            sx={{ mr: 5, display: ["none", "block"] }}
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
              href={loggedIn ? "/:language/profile" : "/:language/login"}
              variant="header"
              sx={{ mr: 5, display: ["block", "none"] }}
            >
              {loggedIn && <FormattedMessage id="header.profile" />}
              {!loggedIn && <FormattedMessage id="header.login" />}
            </Link>

            <Box as="nav">
              <Links links={conferenceMenu!.links} language={language} />
            </Box>
            <Box as="nav">
              {programMenu!.links.map(link => (
                <Link
                  variant="header"
                  href={language === "en" ? link.hrefEn : link.hrefIt}
                  key={language === "en" ? link.hrefEn : link.hrefIt}
                >
                  {language === "en" ? link.titleEn : link.titleIt}
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
