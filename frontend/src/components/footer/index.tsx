/** @jsx jsx */

import { Box, Flex, Grid } from "@theme-ui/components";
import { graphql, Link, useStaticQuery } from "gatsby";
import { jsx } from "theme-ui";

import { Backend_MenuLink, FooterQuery } from "../../generated/graphql";
import { Logo } from "../logo";
import Facebook from "../socials/facebook";
import Instagram from "../socials/instagram";
import Twitter from "../socials/twitter";

const MenuItems: React.SFC = ({ children, ...props }) => (
  <ul
    sx={{
      color: "white",
      listStyle: "none",

      a: {
        color: "white",
        textDecoration: "none",
      },
    }}
    {...props}
  >
    {children}
  </ul>
);

const SocialCircle: React.SFC<{ color: string }> = ({ children, color }) => (
  <li
    sx={{
      width: "40px",
      height: "40px",
      borderRadius: "100%",
      backgroundColor: color,
      flexShrink: 0,
      cursor: "pointer",
      a: {
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        width: "100%",
        height: "100%",
      },
      svg: {
        path: {
          fill: "white",
        },
      },
    }}
  >
    {children}
  </li>
);

export const Footer = () => {
  const {
    backend: {
      conference: { menu },
    },
  } = useStaticQuery<FooterQuery>(graphql`
    query Footer {
      backend {
        conference {
          menu(identifier: "footer-nav") {
            links {
              title
              href
            }
          }
        }
      }
    }
  `);

  const links = menu ? menu.links : [];

  let firstGroup = links;
  let secondGroup: Pick<Backend_MenuLink, "title" | "href">[] = [];

  if (links.length > 4) {
    const halfLinks = Math.round(links.length / 2);
    firstGroup = links.slice(0, halfLinks);
    secondGroup = links.slice(halfLinks);
  }

  return (
    <Box
      sx={{
        background: "black",
        py: [4, 5],
        px: 2,
      }}
    >
      <Grid
        sx={{
          maxWidth: "container",
          mx: "auto",

          gridTemplateColumns: [null, null, "5fr 1fr 2fr 2fr 3fr"],
        }}
      >
        <Logo />

        <MenuItems
          sx={{
            gridColumnStart: [null, null, 3],
          }}
        >
          {firstGroup.map((link, i) => (
            <li key={i}>
              <Link to={link.href}>{link.title}</Link>
            </li>
          ))}
        </MenuItems>

        <MenuItems>
          {secondGroup.map((link, i) => (
            <li key={i}>
              <Link to={link.href}>{link.title}</Link>
            </li>
          ))}
        </MenuItems>

        <Flex
          as="ul"
          sx={{
            listStyle: "none",

            "li + li": {
              marginLeft: 3,
            },
          }}
        >
          <SocialCircle color="#34B4A1">
            <a
              target="_blank"
              rel="noreferrer noopener"
              href="https://twitter.com/pyconit"
            >
              <Twitter />
            </a>
          </SocialCircle>
          <SocialCircle color="#9473B0">
            <a
              target="_blank"
              rel="noreferrer noopener"
              href="https://www.facebook.com/pythonitalia/"
            >
              <Facebook />
            </a>
          </SocialCircle>
          <SocialCircle color="#F17A">
            <a
              target="_blank"
              rel="noreferrer noopener"
              href="https://www.instagram.com/python.it/"
            >
              <Instagram />
            </a>
          </SocialCircle>
        </Flex>
      </Grid>
    </Box>
  );
};
