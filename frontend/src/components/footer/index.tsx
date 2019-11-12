/** @jsx jsx */

import { Box, Grid } from "@theme-ui/components";
import { graphql, Link, useStaticQuery } from "gatsby";
import { jsx } from "theme-ui";

import { Backend_MenuLink, FooterQuery } from "../../generated/graphql";
import { Logo } from "../logo";
import { SocialLinks } from "../social-links";

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
        mt: "auto",
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

        <SocialLinks />
      </Grid>
    </Box>
  );
};
