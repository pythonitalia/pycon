import { Column, Row } from "grigliata";
import React from "react";

import { STANDARD_ROW_PADDING } from "../../config/spacing";
import { MaxWidthWrapper } from "../max-width-wrapper";

export class ErrorBoundary extends React.Component<
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
        <MaxWidthWrapper>
          <Row
            paddingLeft={STANDARD_ROW_PADDING}
            paddingRight={STANDARD_ROW_PADDING}
          >
            <Column
              columnWidth={{
                mobile: 12,
                tabletPortrait: 12,
                tabletLandscape: 12,
                desktop: 12,
              }}
            >
              <h2>Something went wrong.</h2>
              <details style={{ whiteSpace: "pre-wrap" }}>
                {this.state.error && this.state.error.toString()}
                <br />
                {this.state.errorInfo.componentStack}
              </details>
            </Column>
          </Row>
        </MaxWidthWrapper>
      );
    }

    return this.props.children;
  }
}
