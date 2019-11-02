/** @jsx jsx */

import { Box, Button, Flex } from "@theme-ui/components";
import { graphql, useStaticQuery } from "gatsby";
import { jsx } from "theme-ui";

import { HeaderQuery } from "../../generated/graphql";
import { useToggle } from "../../helpers/use-toggle";
import SnakesColumns from "../snakes-columns";

export const Header = () => {
  const [isMenuOpen, toggleMenu] = useToggle(false);
  const {
    logo,
    backend: {
      conference: { menu },
    },
  } = useStaticQuery<HeaderQuery>(graphql`
    query Header {
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

        px: "8px",

        width: "100%",

        zIndex: "header",
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

              px: ["5px", "13px"],
              py: ["5px", "7px"],
            }}
            variant="white"
          >
            <SnakesColumns />
            Menu
          </Button>
        </Flex>
      </Flex>
    </Box>
  );
};
