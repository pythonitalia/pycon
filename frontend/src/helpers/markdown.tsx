import { Heading, Link, Spacer, Text } from "@python-italia/pycon-styleguide";
import marksy from "marksy";
import { createElement } from "react";

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
          <Text color="none" size="inherit" decoration="underline">
            {children}
          </Text>
        </Link>
      );
    },
    h1({ children }) {
      return (
        <>
          <Spacer size="small" />
          <Heading size={1}>{children}</Heading>
          <Spacer size="small" />
        </>
      );
    },
    h2({ children }) {
      return (
        <>
          <Spacer size="small" />
          <Heading size={2}>{children}</Heading>
          <Spacer size="small" />
        </>
      );
    },
    h3({ children }) {
      return (
        <>
          <Spacer size="small" />
          <Heading size={3}>{children}</Heading>
          <Spacer size="small" />
        </>
      );
    },
    h4({ children }) {
      return (
        <>
          <Spacer size="small" />
          <Heading size={4}>{children}</Heading>
          <Spacer size="small" />
        </>
      );
    },
    h5({ children }) {
      return (
        <>
          <Spacer size="small" />
          <Heading size={5}>{children}</Heading>
          <Spacer size="small" />
        </>
      );
    },
    p({ children }) {
      return (
        <Text as="p" size={2}>
          {children}
        </Text>
      );
    },
    li({ children }) {
      return (
        <li>
          <Text size={2}>{children}</Text>
        </li>
      );
    },
  },
});
