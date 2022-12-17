import React from "react";
import { Container } from "../container";
import { SnakeHead } from "../illustrations/snake-head";
import { SnakeTail } from "../illustrations/snake-tail";
import { Heading } from "../heading";
import { Separator } from "../separator";
import { FormattedMessage } from "react-intl";
import { SocialLink, SocialLinkProps } from "./social-link";
import { Link as LinkType } from "../navbar/types";
import { Link } from "../link";
import { Text } from "../text";

type Props = {
  logo: React.ElementType;
  socials: SocialLinkProps[];
  bottomLinks?: LinkType[];
};

export const Footer = ({ logo: Logo, socials, bottomLinks = [] }: Props) => (
  <footer className="overflow-x-clip mt-20 lg:mt-32">
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
    <div className="bg-green">
      <Container>
        <div className="py-8 lg:py-10 flex flex-col gap-4 md:gap-0 md:items-center md:flex-row md:justify-between">
          <Heading size={2}>
            <FormattedMessage
              id="footer.stayTuned"
              defaultMessage="Stay tuned!"
            />
          </Heading>
          <ul className="flex gap-9">
            {socials.map((social) => (
              <li
                key={social.icon}
                className="w-7 h-7 flex items-center justify-center"
              >
                <SocialLink {...social} />
              </li>
            ))}
          </ul>
        </div>
      </Container>
      <Separator />
    </div>
    <div className="bg-green">
      <Container>
        <div className="py-6 lg:py-8 flex flex-col gap-4 md:gap-0 md:flex-row justify-between md:items-center">
          <ul className="flex flex-col lg:flex-row gap-4">
            {bottomLinks.map((link) => (
              <li key={link.link}>
                <Link href={link.link}>
                  <Text size="label3" weight="strong" color="none">
                    {link.text}
                  </Text>
                </Link>
              </li>
            ))}
          </ul>
          <div className="flex flex-col lg:flex-row lg:items-center gap-4">
            <Link target="_blank" href="https://rollstudio.co.uk/">
              <Text size="label4" uppercase weight="strong" color="none">
                <FormattedMessage
                  id="footer.designedBy"
                  defaultMessage="Designed by ROLL Studio"
                />
              </Text>
            </Link>
            <a
              target="_blank"
              href="https://vercel.com/?utm_source=python-italia&utm_campaign=oss"
            >
              <img
                src="https://www.datocms-assets.com/31049/1618983297-powered-by-vercel.svg"
                alt="Powered by Vercel Logo"
              />
            </a>
          </div>
        </div>
      </Container>
      <Separator />
    </div>
  </footer>
);
