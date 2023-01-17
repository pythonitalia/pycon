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
        <>
          <Text as="p" size={2}>
            {children}
          </Text>
        </>
      );
    },
    span({ children }) {
      return (
        <Text as="span" size={2}>
          {children}
        </Text>
      );
    },
    ul({ children }) {
      return (
        <>
          <Spacer size="small" />
          <ul>{children}</ul>
          <Spacer size="small" />
        </>
      );
    },
    li({ children }) {
      return (
        <li>
          <Text size={2}>{children}</Text>
        </li>
      );
    },
    img({ src, alt }) {
      return (
        <>
          <img
            src={src}
            alt={alt}
            style={{
              maxWidth: "300px",
            }}
          />
          <Spacer size="small" />
        </>
      );
    },
    strong({ children }) {
      return (
        <Text as="span" size="inherit" weight="strong">
          {children}
        </Text>
      );
    },
  },
});
