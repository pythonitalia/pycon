import clsx from "clsx";
import React from "react";
import { FormattedMessage } from "react-intl";
import { Container } from "../container";
import { SnakeHead } from "../illustrations/snake-head";
import { SnakeTail } from "../illustrations/snake-tail";
import { Link } from "../link";
import type { Link as LinkType } from "../navbar/types";
import { Separator } from "../separator";
import type { SocialLinkProps } from "../social-links/social-link";
import { SocialLinks } from "../social-links/social-links";
import { Text } from "../text";

type Props = {
  logo: React.ElementType;
  socials: SocialLinkProps[];
  bottomLinks?: LinkType[];
  socialsBarLeft?: React.ReactNode;
  noTopSpace?: boolean;
};

export const Footer = ({
  noTopSpace,
  logo: Logo,
  socials,
  bottomLinks = [],
  socialsBarLeft,
}: Props) => (
  <div className="mt-auto">
    <footer
      className={clsx("overflow-x-clip bg-green", {
        "mt-20 lg:mt-32": !noTopSpace,
      })}
    >
      <div className="bg-caramel">
        <Separator />
        <Container>
          <div className="py-8 lg:py-10 relative flex items-center justify-between">
            <div className="flex items-center w-36 h-14 lg:w-56 lg:h-24">
              <Logo />
            </div>

            <div className="flex absolute scale-125 -top-[5px] lg:-top-[46px] right-0 lg:scale-100">
              <SnakeHead className="w-24 h-full lg:w-48" />
              <SnakeTail className="w-16 h-full lg:w-36 mt-auto -mb-[1px] rotate-180" />
            </div>
          </div>
        </Container>
        <Separator />
      </div>
      <div>
        <Container>
          <div className="py-8 lg:py-10 flex flex-col gap-4 md:gap-0 md:items-center md:flex-row md:justify-between">
            {socialsBarLeft}
            <SocialLinks className="hidden md:flex" socials={socials} />
          </div>
        </Container>
        <Separator />
      </div>
      <div className="md:hidden">
        <Container>
          <div className="py-8 lg:py-10 relative flex items-center justify-between">
            <SocialLinks socials={socials} />
          </div>
        </Container>
        <Separator />
      </div>
      <div>
        <Container>
          <div className="py-6 lg:py-8 flex flex-col gap-4 md:gap-0 md:flex-row justify-between md:items-center">
            <ul className="flex flex-col lg:flex-row gap-4">
              {bottomLinks.map((link) => (
                <li key={link.link}>
                  <Link hoverColor="cream" href={link.link}>
                    <Text size="label3" weight="strong" color="none">
                      {link.text}
                    </Text>
                  </Link>
                </li>
              ))}
            </ul>
            <div className="flex flex-col lg:flex-row lg:items-center gap-4">
              <Link
                hoverColor="cream"
                target="_blank"
                href="https://rollstudio.co.uk/"
              >
                <Text size="label4" uppercase weight="strong" color="none">
                  <FormattedMessage
                    id="footer.designedBy"
                    defaultMessage="Designed by ROLL Studio"
                  />
                </Text>
              </Link>
              <Link
                hoverColor="cream"
                target="_blank"
                href="https://github.com/pythonitalia/pycon"
              >
                <Text size="label4" uppercase weight="strong" color="none">
                  <FormattedMessage
                    id="footer.builtBy"
                    defaultMessage="Built by Python Italia"
                  />
                </Text>
              </Link>
            </div>
          </div>
        </Container>
        <Separator />
      </div>
    </footer>
  </div>
);
