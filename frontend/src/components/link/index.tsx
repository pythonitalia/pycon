/** @jsx jsx */
import NextLink from "next/link";
import React from "react";
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

type Params = {
  [param: string]: string;
};

type LinkProps = {
  url?: string;
  path: string;
  variant?: string;
  target?: string;
  backgroundColor?: string;
  after?: React.ReactElement | null;
  params?: Params;
};

export const Link: React.FC<LinkProps> = ({
  children,
  path,
  backgroundColor,
  after,
  target,
  variant,
  url,
  params = null,
  ...additionalProps
}) => {
  const language = useCurrentLanguage();

  if (!url) {
    url = path.replace("[lang]", language);

    Object.entries(params || {}).forEach(([param, value]) => {
      url = url.replace(`[${param}]`, value);
    });
  }

  const ForwardedLink = React.forwardRef<any, { hovered: boolean }>(
    (props, ref) => (
      <ThemeLink
        as="a"
        target={target}
        variant={variant}
        href={path}
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
      </ThemeLink>
    ),
  );

  const component = (hovered: boolean) => <ForwardedLink hovered={hovered} />;

  const [hoverable, _] = useHover(component);

  if (isExternalLink({ path, target })) {
    return hoverable;
  }

  return (
    <NextLink as={url} href={path} passHref={true}>
      {hoverable}
    </NextLink>
  );
};
