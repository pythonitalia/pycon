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
      {children}
    </ThemeLink>
  );
};
