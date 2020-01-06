/** @jsx jsx */
import { isRedirect } from "@reach/router";
import { Box } from "@theme-ui/components";
import { Component } from "react";
import { jsx } from "theme-ui";
import * as Sentry from "@sentry/browser";

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
    Sentry.withScope(scope => {
      scope.setExtras(errorInfo);
      const eventId = Sentry.captureException(error);
      this.setState({ eventId });
    });

    if (isRedirect(error)) {
      throw error;
    } else {
      this.setState({
        error,
        errorInfo,
      });
    }
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
