/** @jsx jsx */

import { Box } from "@theme-ui/components";
import { ColorPalette, TypeScale, TypeStyle } from "@theme-ui/style-guide";
import { jsx, Styled } from "theme-ui";

export default () => (
  <Box
    sx={{
      maxWidth: "container",
      mx: "auto",
      mt: 3,
    }}
  >
    <Styled.h1>Style Guide</Styled.h1>

    <ColorPalette />

    <TypeScale />

    <TypeStyle fontFamily="heading" fontWeight="heading" lineHeight="heading" />
    <TypeStyle fontFamily="body" fontWeight="body" lineHeight="body" />
  </Box>
);
