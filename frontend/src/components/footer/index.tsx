/** @jsxRuntime classic */

/** @jsx jsx */
import { Box, Grid, jsx, Flex } from "theme-ui";

import { LogoBlack } from "../icons/logo-black";
import { Link } from "../link";
import { SocialLinks } from "../social-links";

export const Footer = () => {
  return (
    <Box
      sx={
        {
          background: "black",
          py: [4, 5],
          px: 3,
          mt: "auto",
          zIndex: "footer",
          "@media print": {
            display: "none",
          },
        } as any
      }
    >
      <Grid
        sx={{
          maxWidth: "container",
          mx: "auto",
          gridTemplateColumns: [null, null, "1fr 1fr"],
        }}
      >
        <Link path="/">
          <LogoBlack
            sx={{
              width: "100%",
              maxWidth: 300,
              display: "block",
              mx: ["auto", null, 0],
            }}
          />
        </Link>

        <Flex
          sx={{
            flexDirection: "column",
            alignItems: ["center", "center", "flex-end"],
          }}
        >
          <SocialLinks sx={{ justifyContent: ["center", null, "flex-end"] }} />
          <a
            target="_blank"
            href="https://vercel.com/?utm_source=python-italia&utm_campaign=oss"
            sx={{
              mt: 4,
            }}
          >
            <img
              src="https://www.datocms-assets.com/31049/1618983297-powered-by-vercel.svg"
              alt="Powered by Vercel Logo"
            />
          </a>
        </Flex>
      </Grid>
    </Box>
  );
};
