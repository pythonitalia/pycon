/** @jsxRuntime classic */
/** @jsx jsx */
import { Box, Grid, jsx } from "theme-ui";

import { useFooterQuery } from "~/types";

import { LogoBlack } from "../icons/logo-black";
import { Link } from "../link";
import { SocialLinks } from "../social-links";

const MenuItems: React.SFC = ({ children, ...props }) => (
  <Box
    as="ul"
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
  </Box>
);

export const Footer = () => {
  const { data } = useFooterQuery({
    variables: {
      code: process.env.conferenceCode,
    },
  });

  if (!data) {
    return null;
  }

  const {
    conference: { menu },
  } = data;

  const links = menu ? menu.links : [];

  let firstGroup = links;
  let secondGroup: { title: string; href: string }[] = [];

  if (links.length > 4) {
    const halfLinks = Math.round(links.length / 2);
    firstGroup = links.slice(0, halfLinks);
    secondGroup = links.slice(halfLinks);
  }

  return (
    <Box
      sx={
        {
          background: "black",
          py: [4, 5],
          px: 3,
          mt: "auto",
          zIndex: "footer",
        } as any
      }
    >
      <Grid
        sx={{
          maxWidth: "container",
          mx: "auto",
          gridTemplateColumns: [null, null, "5fr 1fr 2fr 2fr 3fr"],
        }}
      >
        <Link path="/[lang]">
          <LogoBlack
            sx={{
              width: "100%",
              maxWidth: 300,
              display: "block",
              mx: ["auto", null, 0],
            }}
          />
        </Link>

        <MenuItems
          sx={{
            gridColumnStart: [null, null, 3],
          }}
        >
          {firstGroup.map((link, i) => (
            <li key={i}>
              <Link path={link.href}>{link.title}</Link>
            </li>
          ))}
        </MenuItems>

        <MenuItems>
          {secondGroup.map((link, i) => (
            <li key={i}>
              <Link path={link.href}>{link.title}</Link>
            </li>
          ))}
        </MenuItems>

        <SocialLinks sx={{ justifyContent: ["center", null, "flex-end"] }} />
      </Grid>
    </Box>
  );
};
