/** @jsx jsx */
import { Box, Heading } from "@theme-ui/components";
import * as React from "react";
import { jsx } from "theme-ui";

const NotFoundPage = () => {
  React.useEffect(() => {
    if (typeof window !== "undefined" && window.location.pathname === "/en/blog/%20pycon-11-cancelled/") {
      window.location.href = "https://pycon.it/en/blog/pycon-11-cancelled/"
    }
  }, [])
  
  return (
    <Box sx={{ mx: "auto", maxWidth: "container", p: 3 }}>
      <Heading sx={{ fontSize: 5 }} as="h1">
        Page not found!
      </Heading>
    </Box>
  );
}

export default NotFoundPage;
