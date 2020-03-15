/** @jsx jsx */
import { Flex } from "@theme-ui/components";
import { jsx } from "theme-ui";

import Facebook from "../icons/social/facebook";
import Instagram from "../icons/social/instagram";
import Twitter from "../icons/social/twitter";
import { SocialCircle } from "./social-circle";

type SocialLinksProps = {
  variant?: string;
};

export const SocialLinks: React.SFC<SocialLinksProps> = (props) => (
  <Flex
    as="ul"
    sx={{
      listStyle: "none",

      "li + li": {
        marginLeft: 3,
      },
    }}
    {...props}
  >
    <SocialCircle variant={props.variant} color="#34B4A1">
      <a
        target="_blank"
        rel="noreferrer noopener"
        href="https://twitter.com/pyconit"
      >
        <Twitter />
      </a>
    </SocialCircle>
    <SocialCircle variant={props.variant} color="#9473B0">
      <a
        target="_blank"
        rel="noreferrer noopener"
        href="https://www.facebook.com/pythonitalia/"
      >
        <Facebook />
      </a>
    </SocialCircle>
    <SocialCircle variant={props.variant} color="#F17A">
      <a
        target="_blank"
        rel="noreferrer noopener"
        href="https://www.instagram.com/python.it/"
      >
        <Instagram />
      </a>
    </SocialCircle>
  </Flex>
);
