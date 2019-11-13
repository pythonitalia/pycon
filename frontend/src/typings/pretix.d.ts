import * as React from "react";

type PretixWidgetProps = {
  event: string;
};

declare global {
  namespace JSX {
    interface IntrinsicElements {
      "pretix-widget": React.DetailedHTMLProps<
        React.HTMLAttributes<HTMLElement> & PretixWidgetProps,
        HTMLElement
      >;
    }
  }
}
