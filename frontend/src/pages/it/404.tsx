/** @jsx jsx */
import { Box, Heading } from "@theme-ui/components";
import * as React from "react";
import { jsx } from "theme-ui";

const NotFoundPage = () => (
  <Box sx={{ mx: "auto", maxWidth: "container", p: 3 }}>
    <Heading sx={{ fontSize: 5 }} as="h1">
      Pagina non trovata!
    </Heading>
  </Box>
);

export default NotFoundPage;
