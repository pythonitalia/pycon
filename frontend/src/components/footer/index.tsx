/** @jsx jsx */

import { Box, Flex, Grid } from "@theme-ui/components";
import { graphql, Link, useStaticQuery } from "gatsby";
import { jsx } from "theme-ui";

import { Backend_MenuLink, FooterQuery } from "../../generated/graphql";
import { Logo } from "../logo";

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
        py: [4, 6],
        px: 2,
      }}
    >
      <Grid
        sx={{
          maxWidth: "container",
          mx: "auto",

          gridTemplateColumns: [null, "6fr 5fr 2fr 2fr 3fr"],
        }}
      >
        <Logo />

        <MenuItems
          sx={{
            gridColumnStart: [null, 3],
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
              marginLeft: 4,
            },
          }}
        >
          <li
            sx={{
              width: "40px",
              height: "40px",
              borderRadius: "100%",
              backgroundColor: "#34B4A1",
            }}
          />
          <li
            sx={{
              width: "40px",
              height: "40px",
              borderRadius: "100%",
              backgroundColor: "#9473B0",
            }}
          />
          <li
            sx={{
              width: "40px",
              height: "40px",
              borderRadius: "100%",
              backgroundColor: "#F17A5D",
            }}
          />
        </Flex>
      </Grid>
    </Box>
  );
};
