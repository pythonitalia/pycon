import {
  Heading,
  Link,
  Page,
  Section,
  Text,
} from "@python-italia/pycon-styleguide";
import * as Sentry from "@sentry/nextjs";
import React, { Component } from "react";

type Props = {
  children: React.ReactNode;
};

export class ErrorBoundary extends Component<
  Props,
  {
    errorInfo: any | null;
    error: string | null;
    eventId: any | null;
  }
> {
  constructor(props: Readonly<Props>) {
    super(props);
    this.state = { error: null, errorInfo: null, eventId: null };
  }

  componentDidCatch(error: any, errorInfo: any) {
    Sentry.withScope((scope) => {
      scope.setExtras(errorInfo);
      const eventId = Sentry.captureException(error);
      this.setState({ eventId });

      this.setState({
        error,
        errorInfo,
      });
    });
  }

  render() {
    if (this.state.errorInfo) {
      return (
        <Page endSeparator={false}>
          <Section>
            <Heading size={2}>Something went wrong.</Heading>

            <Text>
              If a refresh doesn't work, please report this to{" "}
              <Link
                target="_blank"
                href="https://github.com/pythonitalia/pycon"
              >
                <Text
                  size="inherit"
                  color="none"
                  decoration="underline"
                  weight="strong"
                >
                  our repo on github.
                </Text>
              </Link>
            </Text>

            <video
              muted
              loop
              autoPlay
              src="/videos/sad.mp4"
              style={{
                position: "fixed",
                top: 0,
                left: 0,
                height: "100vh",
                width: "100vw",
                zIndex: 0,
                pointerEvents: "none",
                objectFit: "cover",
                opacity: 0.5,
              }}
            />

            <details style={{ whiteSpace: "pre-wrap" }}>
              {this.state.error && this.state.error.toString()}
              <br />
              {this.state.errorInfo.componentStack}
            </details>
          </Section>
        </Page>
      );
    }

    return this.props.children;
  }
}
