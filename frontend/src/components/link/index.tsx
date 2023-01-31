/** @jsxRuntime classic */

/** @jsx jsx */
import { ParsedUrlQuery } from "querystring";
import React from "react";
import {
  Box,
  Flex,
  jsx,
  Link as ThemeLink,
  ThemeUIStyleObject,
} from "theme-ui";

import { useCurrentLanguage } from "~/locale/context";

const ArrowRightBackground = ({
  children,
}: React.PropsWithChildren<unknown>) => (
  <Flex
    sx={{
      top: 0,
      left: 0,
      height: 51,
      "&:hover": {
        "div, .arrow-sec": {
          backgroundColor: "orange",
          fill: "orange",
        },
      },
    }}
  >
    <Box
      sx={{
        borderTop: "primary",
        borderBottom: "primary",
        borderLeft: "primary",
        height: 51,
        backgroundColor: "yellow",
      }}
    >
      {children}
    </Box>
    <svg
      viewBox="2 0 32 66"
      preserveAspectRatio="none"
      vectorEffect="non-scaling-stroke"
      sx={{
        height: 51,
        right: 0,
      }}
    >
      <path d="M1 0V66L30 33L1 0Z" stroke="black" strokeWidth="5" />
      <path
        className="arrow-sec"
        d="M0 2.5L27.5 33L0 63.5V2.5Z"
        sx={{ fill: "yellow" }}
      />
    </svg>
  </Flex>
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
  as?: any;
  onClick?: (event) => void;
  sx?: ThemeUIStyleObject;
};

export const Link = ({
  children,
  path,
  backgroundColor,
  target,
  variant,
  external = false,
  params = null,
  locale,
  ...additionalProps
}: React.PropsWithChildren<LinkProps>) => {
  const language = useCurrentLanguage();
  const normalizedLocale = locale || language;
  const isExternal = external || isExternalLink({ path, target });
  const href = createHref({
    path,
    params,
    locale: normalizedLocale,
    external: isExternal,
  });

  const ForwardedLink = React.forwardRef<any>((props, ref) => (
    <ThemeLink
      variant={variant}
      href={href}
      target={target}
      sx={
        variant === "arrow-button"
          ? {
              p: 0,
              border: 0,
            }
          : {}
      }
      {...props}
      {...additionalProps}
      ref={ref}
    >
      {variant === "arrow-button" && (
        <ArrowRightBackground>
          <Box
            as="span"
            sx={{
              zIndex: 10,
              px: 3,
            }}
          >
            {children}
          </Box>
        </ArrowRightBackground>
      )}
      {variant !== "arrow-button" && children}
    </ThemeLink>
  ));

  return <ForwardedLink />;
};

export const createHref = ({
  path,
  params,
  locale,
  external,
}: {
  path: string;
  params?: ParsedUrlQuery;
  locale: string;
  external?: boolean;
}) => {
  if (external) {
    return path;
  }

  const { resolvedPath, unusedParams } = Object.entries(params || {}).reduce(
    (state, [key, value]) => {
      const newPath = state.resolvedPath.replace(`[${key}]`, value as string);

      if (newPath === state.resolvedPath) {
        state.unusedParams[key] = value;
        return state;
      }

      state.resolvedPath = newPath;
      return state;
    },
    {
      resolvedPath: path,
      unusedParams: {},
    },
  );

  const queryParams = Object.entries(unusedParams)
    .map(([key, value]) => `${key}=${value}`)
    .join("&");

  return `/${locale}${resolvedPath}${
    queryParams.length > 0 ? `?${queryParams}` : ""
  }`;
};
