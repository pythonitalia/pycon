/** @jsx jsx */

import { Box, Button, Flex } from "@theme-ui/components";
import { graphql, useStaticQuery } from "gatsby";
import { jsx } from "theme-ui";

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
    <Box
      sx={{
        position: "absolute",
        top: ["30px", "60px"],
        left: "0px",

        px: "32px",

        width: "100%",

        zIndex: "navbar",
      }}
    >
      <Flex
        sx={{
          maxWidth: "largeContainer",
          mx: "auto",

          justifyContent: "space-between",
          alignItems: "center",
        }}
      >
        <img
          sx={{
            width: ["150px", "300px"],
          }}
          src={logo!.publicURL!}
        />

        <Box>
          <Button>Login</Button>
          <Button>Menu</Button>
        </Box>
      </Flex>
    </Box>
  );
};
