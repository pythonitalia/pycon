/** @jsx jsx */

import { Box, Button, Flex } from "@theme-ui/components";
import { graphql, useStaticQuery } from "gatsby";
import { jsx } from "theme-ui";

import { HeaderQuery } from "../../generated/graphql";
import { Logo } from "../logo";
import { SnakeBurger } from "./snake-burger";

export const Header = () => {
  const {
    backend: {
      conference: { menu },
    },
  } = useStaticQuery<HeaderQuery>(graphql`
    query Header {
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
        top: [3, 4, 5],
        left: 0,

        px: 2,

        width: "100%",

        zIndex: "header",
      }}
    >
      <Flex
        sx={{
          maxWidth: "largeContainer",
          mx: "auto",

          justifyContent: "space-between",
          alignItems: ["center", "flex-start"],
        }}
      >
        <Logo
          sx={{
            width: ["37vw", "33vw", "25vw", "15vw"],
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
            variant="white"
          >
            <SnakeBurger />
            Menu
          </Button>
        </Flex>
      </Flex>
    </Box>
  );
};
