/** @jsx jsx */
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
});
