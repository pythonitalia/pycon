/** @jsx jsx */
import { isRedirect } from "@reach/router";
import * as Sentry from "@sentry/browser";
import { Box } from "@theme-ui/components";
import { Component } from "react";
import { jsx } from "theme-ui";

const SENTRY_DSN = process.env.SENTRY_DSN || "";
console.log({ SENTRY_DSN });
console.log({ process });
Sentry.init({ dsn: SENTRY_DSN });

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
  }

  componentDidCatch(error: any, errorInfo: any) {
    console.warn("ErrorBoundary: componentDidCatch!!");
    console.log(isRedirect(error));
    Sentry.captureMessage("Something went wrong (from @Etty with <3)");

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
        <Box sx={{ mx: "auto", maxWidth: "container", pb: 6 }}>
          <h2>Something went wrong.</h2>
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
