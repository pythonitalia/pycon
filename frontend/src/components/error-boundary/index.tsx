/** @jsx jsx */
import { Box } from "@theme-ui/components";
import { Component } from "react";
import { jsx } from "theme-ui";

export class ErrorBoundary extends Component<
  {},
  {
    errorInfo: any | null;
    error: string | null;
  }
> {
  constructor(props: Readonly<{}>) {
    super(props);

    this.state = { error: null, errorInfo: null };
  }

  componentDidCatch(error: any, errorInfo: any) {
    this.setState({
      error,
      errorInfo,
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
