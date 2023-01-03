/** @jsxRuntime classic */

/** @jsx jsx */
import { Link } from "@python-italia/pycon-styleguide";
import marksy from "marksy";
import { createElement } from "react";
import { jsx } from "theme-ui";

import { MapWithLink } from "../components/map-with-link";

export const compile = marksy({
  createElement,
  components: {
    Map() {
      return <MapWithLink />;
    },
  },
  elements: {
    a({ href, children, target }) {
      return (
        <Link target={target} href={href}>
          {children}
        </Link>
      );
    },
  },
});
