/** @jsx jsx */
import { Box, Heading, jsx } from "theme-ui";

const Error = ({ statusCode }) => (
  <Box sx={{ mt: 4, mx: "auto", maxWidth: "container", px: 3, pb: 6 }}>
    <Heading as="h2" sx={{ mb: 2 }}>
      Error {statusCode}
    </Heading>

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

Error.getInitialProps = ({ res, err }) => {
  const statusCode = res ? res.statusCode : err ? err.statusCode : 404;
  return { statusCode };
};

export default Error;
