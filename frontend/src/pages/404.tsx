/** @jsxRuntime classic */

/** @jsx jsx */
import { FormattedMessage } from "react-intl";
import { Box, Heading, jsx, Text } from "theme-ui";

import { Link } from "~/components/link";

const Error404 = () => (
  <Box sx={{ mt: 4, mx: "auto", maxWidth: "container", px: 3, pb: 6 }}>
    <Heading as="h2" sx={{ mb: 2 }}>
      We can't find the page you are looking for!
    </Heading>

    <Text as="div">
      <Link path="/[lang]" sx={{ display: "block", mt: 2 }}>
        <FormattedMessage id="error404.goToHomepage" />
      </Link>
    </Text>

    <video
      sx={{
        position: "absolute",
        top: 0,
        left: 0,
        height: "100vh",
        width: "100vw",
        zIndex: -1,
        pointerEvents: "none",
        objectFit: "cover",
        opacity: 0.5,
      }}
      src="/videos/sad.mp4"
      autoPlay={true}
      muted={true}
      loop={true}
    />
  </Box>
);

export default Error404;
