/** @jsxRuntime classic */
/** @jsx jsx */
import * as Sentry from "@sentry/node";
import NextErrorComponent from "next/error";
import { FormattedMessage } from "react-intl";
import { Box, Heading, jsx, Text } from "theme-ui";

import { Link } from "~/components/link";

const ErrorPage = ({ statusCode }) => (
  <Box sx={{ mt: 4, mx: "auto", maxWidth: "container", px: 3, pb: 6 }}>
    <Heading as="h2" sx={{ mb: 2 }}>
      Ops {statusCode}
    </Heading>

    {statusCode === 404 && (
      <Text>
        <FormattedMessage id="error404.message" />
        <Link path="/[lang]/" sx={{ display: "block", mt: 2 }}>
          <FormattedMessage id="error404.goToHomepage" />
        </Link>
      </Text>
    )}

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

ErrorPage.getInitialProps = async ({ res, err, asPath }) => {
  // https://github.com/vercel/next.js/issues/8592
  // @ts-ignore
  const errorInitialProps = await NextErrorComponent.getInitialProps({
    res,
    err,
  });

  // @ts-ignore
  errorInitialProps.hasGetInitialPropsRun = true;

  if (res?.statusCode === 404) {
    return { statusCode: 404 };
  }

  if (err) {
    Sentry.captureException(err);
    await Sentry.flush(2000);
    return errorInitialProps;
  }

  Sentry.captureException(
    new Error(`_error.js getInitialProps missing data at path: ${asPath}`),
  );
  await Sentry.flush(2000);
  return errorInitialProps;
};

export default ErrorPage;
