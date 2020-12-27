import * as React from "react";

const { useState } = React;

// eslint-disable-next-line no-empty-function
const noop = () => {};

export type Element =
  | ((state: boolean) => React.ReactElement<any>)
  | React.ReactElement<any>;

export const useHover = (
  element: Element,
): [React.ReactElement<any>, boolean] => {
  const [state, setState] = useState(false);

  const onMouseEnter = (originalOnMouseEnter?: any) => (event: any) => {
    (originalOnMouseEnter || noop)(event);
    setState(true);
  };
  const onMouseLeave = (originalOnMouseLeave?: any) => (event: any) => {
    (originalOnMouseLeave || noop)(event);
    setState(false);
  };

  if (typeof element === "function") {
    element = element(state);
  }

  const el = React.cloneElement(element, {
    onMouseEnter: onMouseEnter(element.props.onMouseEnter),
    onMouseLeave: onMouseLeave(element.props.onMouseLeave),
  });

  return [el, state];
};
