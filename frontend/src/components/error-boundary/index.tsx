/** @jsx jsx */
import { isRedirect } from "@reach/router";
import * as Sentry from "@sentry/browser";
import { Box, Heading, Text } from "@theme-ui/components";
import { Component } from "react";
import { jsx } from "theme-ui";

import { Link } from "../link";

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
    Sentry.withScope(scope => {
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
            <Link href="https://github.com/pythonitalia/pycon">
              our repo on github.
            </Link>
          </Text>

          {
            // TODO: Make this responsive
          }
          <Box
            as="iframe"
            sx={{ mb: 3, width: "100%", maxWidth: "480" }}
            src="https://giphy.com/embed/k61nOBRRBMxva"
            width="480"
            height="326"
            frameBorder="0"
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
