/** @jsxRuntime classic */

/** @jsx jsx */
import { ParsedUrlQuery } from "querystring";
import React, { Fragment } from "react";
import { Box, jsx, Link as ThemeLink } from "theme-ui";

import { useHover } from "~/helpers/use-hover";
import { useCurrentLanguage } from "~/locale/context";

import { GoogleIcon } from "../icons/google";

const ArrowRightBackground = ({
  backgroundColor,
}: {
  backgroundColor: string;
}) => (
  <Box
    sx={{
      position: "absolute",
      top: 0,
      left: 0,
      height: 50,
      width: "calc(100% + 25px)",
    }}
  >
    <Box
      sx={{
        position: "absolute",
        top: "-4px",
        left: 0,
        right: 24,
        borderTop: "primary",
        borderBottom: "primary",
        borderLeft: "primary",
        height: 50,
        backgroundColor,
      }}
    />
    <svg
      viewBox="2 0 32 66"
      preserveAspectRatio="none"
      vectorEffect="non-scaling-stroke"
      sx={{
        position: "absolute",
        top: "-4px",
        height: 50,
        right: 0,
      }}
    >
      <path d="M1 0V66L30 33L1 0Z" stroke="black" strokeWidth="5" />
      <path d="M0 2.5L27.5 33L0 63.5V2.5Z" sx={{ fill: backgroundColor }} />
    </svg>
  </Box>
);

const isExternalLink = ({ path, target }: { path: string; target?: string }) =>
  path.startsWith("http") || path.startsWith("mailto") || target === "_blank";

type LinkProps = {
  path: string;
  variant?: string;
  target?: string;
  locale?: "it" | "en";
  backgroundColor?: string;
  params?: ParsedUrlQuery;
  external?: boolean;
  rel?: string;
  noHover?: boolean;
};

export const Link: React.FC<LinkProps> = ({
  children,
  path,
  backgroundColor,
  target,
  variant,
  external = false,
  params = null,
  locale,
  noHover = false,
  ...additionalProps
}) => {
  const language = useCurrentLanguage();
  const normalizedLocale = locale || language;
  const href = createHref({ path, params, locale: normalizedLocale });

  const ForwardedLink = React.forwardRef<any, { hovered: boolean }>(
    (props, ref) => (
      <ThemeLink
        as="a"
        target={target}
        variant={variant}
        href={href}
        {...props}
        {...additionalProps}
        ref={ref}
      >
        {variant === "arrow-button" && (
          <ArrowRightBackground
            backgroundColor={
              props.hovered ? "orange" : backgroundColor || "yellow"
            }
          />
        )}

        {variant === "google" && <GoogleIcon />}

        {noHover && <Fragment>{children}</Fragment>}

        {!noHover && (
          <Box
            as="span"
            sx={{
              position: "relative",
              zIndex: 10,
            }}
          >
            {children}
            {props.hovered}
          </Box>
        )}
      </ThemeLink>
    ),
  );

  const component = (hovered: boolean) => <ForwardedLink hovered={hovered} />;

  const [hoverable] = useHover(component);

  if (external || isExternalLink({ path, target })) {
    return hoverable;
  }

  return (
    <a href={href} {...additionalProps}>
      {hoverable}
    </a>
  );
};

const createHref = ({ path, params, locale }) => {
  const { resolvedPath, unusedParams } = Object.entries(params || {}).reduce(
    (state, [key, value]) => {
      const newPath = state.resolvedPath.replace(`[${key}]`, value);

      if (newPath === state.resolvedPath) {
        state.unusedParams[key] = value;
        return state;
      }

      state.resolvedPath = newPath;
      return state;
    },
    { resolvedPath: path, unusedParams: {} },
  );

  const queryParams = Object.entries(unusedParams)
    .map(([key, value]) => `${key}=${value}`)
    .join("&");

  return `/${locale}${resolvedPath}?${queryParams}`;
};
