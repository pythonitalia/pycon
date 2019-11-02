import { Box, Button, Flex } from "@theme-ui/components";
import { graphql, useStaticQuery } from "gatsby";
import React from "react";

import { NavBarQuery } from "../../generated/graphql";
import { useToggle } from "../../helpers/use-toggle";

export const Topbar = () => {
  const [isMenuOpen, toggleMenu] = useToggle(false);
  const {
    logo,
    backend: {
      conference: { menu },
    },
  } = useStaticQuery<NavBarQuery>(graphql`
    query NavBar {
      logo: file(name: { eq: "logo" }) {
        publicURL
      }

      backend {
        conference {
          menu(identifier: "header-nav") {
            links {
              title
              href
              isPrimary
            }
          }
        }
      }
    }
  `);

  const { links } = menu!;

  return (
    <Flex
      sx={{
        justifyContent: "space-between",
        alignItems: "center",
        maxWidth: "largeContainer",

        mx: "auto",
      }}
    >
      <img src={logo!.publicURL!} />
      <Box>
        <Button>Login</Button>
        <Button>Menu</Button>
      </Box>
    </Flex>
  );
};
