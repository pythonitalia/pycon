/** @jsx jsx */
import { Box, Link as ThemeLink } from "@theme-ui/components";
import { Link as GatsbyLink } from "gatsby";
import { jsx } from "theme-ui";

import { useCurrentLanguage } from "../../context/language";

type LinkProps = {
  href: string | null;
  variant?: string;
  target?: string;
};

const ArrowRightBackground = ({ ...props }) => (
  <svg
    viewBox="0 0 146 66"
    preserveAspectRatio="none"
    vectorEffect="non-scaling-stroke"
    {...props}
  >
    <path
      d="M2 2h115.065l26.312 31-26.312 31H2V2z"
      stroke="#000"
      strokeWidth={4}
    />
  </svg>
);

export const Link: React.SFC<LinkProps> = ({
  children,
  href,
  ...additionalProps
}) => {
  const language = useCurrentLanguage();
  const isExternal = href && href.startsWith("http");
  const LinkComponent = isExternal
    ? ThemeLink
    : ({ ...props }: { to: string }) => (
        <GatsbyLink activeClassName="active" {...props} />
      );

  if (additionalProps.target === "_blank") {
    (additionalProps as any).rel = "noopener noreferrer";
  }

  if (!isExternal && href) {
    href = href.replace(":language", language);
  }

  return (
    <ThemeLink {...additionalProps} as={LinkComponent} href={href} to={href}>
      {additionalProps.variant === "button" && (
        <ArrowRightBackground
          sx={{
            position: "absolute",
            top: 0,
            left: 0,
            height: "100%",
            width: "calc(100% + 25px)",
            fill: "yellow",
            stroke: "black",
          }}
        />
      )}

      <Box as="span" sx={{ position: "relative", zIndex: 10 }}>
        {children}
      </Box>
    </ThemeLink>
  );
};
