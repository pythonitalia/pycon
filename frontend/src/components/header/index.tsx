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
        <Logo
          sx={{
            width: ["150px", "300px"],
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

              px: ["5px", "13px"],
              py: ["5px", "7px"],
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
