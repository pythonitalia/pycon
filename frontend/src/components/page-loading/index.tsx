/** @jsx jsx */
import { Box, Heading } from "@theme-ui/components";
import { jsx } from "theme-ui";

export const PageLoading: React.SFC = () => (
  <Box sx={{ mx: "auto", py: 5, px: 3, maxWidth: "container" }}>
    <Heading sx={{ fontSize: 4 }}>Loading ⌛</Heading>
  </Box>
);
