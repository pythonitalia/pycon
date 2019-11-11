/** @jsx jsx */
import { Box, Link as ThemeLink } from "@theme-ui/components";
import { Link as GatsbyLink } from "gatsby";
import { jsx } from "theme-ui";

type LinkProps = {
  href: string;
  variant?: string;
  target?: string;
};

export const Link: React.SFC<LinkProps> = ({
  children,
  href,
  ...additionalProps
}) => {
  const isExternal = href && href.startsWith("http");
  const LinkComponent = isExternal
    ? ThemeLink
    : ({ ...props }: { to: string }) => (
        <GatsbyLink activeClassName="active" {...props} />
      );

  if (additionalProps.target === "_blank") {
    (additionalProps as any).rel = "noopener noreferrer";
  }

  return (
    <ThemeLink {...additionalProps} as={LinkComponent} href={href} to={href}>
      {children}
    </ThemeLink>
  );
};
