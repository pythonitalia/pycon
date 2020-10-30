
/** @jsx jsx */

import * as Sentry from "@sentry/browser";
import { Component } from "react";
import { Box, Heading, jsx, Text } from "theme-ui";

import { Link } from "../link";

const isRedirect = (e: any) => false;

export class ErrorBoundary extends Component<
  {},
  {
    errorInfo: any | null;
    error: string | null;
    eventId: any | null;
  }
> {
  constructor(props: Readonly<{}>) {
    super(props);
    this.state = { error: null, errorInfo: null, eventId: null };

    Sentry.init({ dsn: process.env.SENTRY_DSN });
  }

  componentDidCatch(error: any, errorInfo: any) {
    Sentry.withScope((scope) => {
      scope.setExtras(errorInfo);
      const eventId = Sentry.captureException(error);
      this.setState({ eventId });

      if (isRedirect(error)) {
        throw error;
      } else {
        this.setState({
          error,
          errorInfo,
        });
      }
    });
  }

  render() {
    if (this.state.errorInfo) {
      return (
        <Box sx={{ mt: 4, mx: "auto", maxWidth: "container", px: 3, pb: 6 }}>
          <Heading as="h2" sx={{ mb: 2 }}>
            Something went wrong.
          </Heading>

          <Text sx={{ mb: 3 }}>
            If a refresh doesn't work, please report this to{" "}
            <Link path="https://github.com/pythonitalia/pycon">
              our repo on github.
            </Link>
          </Text>

          <Box
            as="video"
            sx={{
              position: "fixed",
              top: 0,
              left: 0,
              height: "100vh",
              width: "100vw",
              zIndex: -1,
              pointerEvents: "none",
              objectFit: "cover",
              opacity: 0.5,
            }}
            {...{
              muted: true,
              lopp: true,
              autoPlay: true,
              src: "/videos/sad.mp4",
            }}
          />

          <details style={{ whiteSpace: "pre-wrap" }}>
            {this.state.error && this.state.error.toString()}
            <br />
            {this.state.errorInfo.componentStack}
          </details>
        </Box>
      );
    }

    return this.props.children;
  }
}
