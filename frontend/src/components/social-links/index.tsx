/** @jsxRuntime classic */

/** @jsx jsx */
import { Flex, jsx } from "theme-ui";

import Facebook from "../icons/social/facebook";
import Instagram from "../icons/social/instagram";
import Linkedin from "../icons/social/linkedin";
import Twitter from "../icons/social/twitter";
import { SocialCircle } from "./social-circle";

type SocialLinksProps = {
  variant?: string;
};

export const SocialLinks: React.FC<SocialLinksProps> = (props) => (
  <Flex
    as="ul"
    sx={{
      listStyle: "none",
      pl: 0,

      "li + li": {
        marginLeft: 3,
      },
    }}
    {...props}
  >
    <SocialCircle variant={props.variant} color="#1D9BF0">
      <a
        target="_blank"
        rel="noreferrer noopener"
        href="https://twitter.com/pyconit"
      >
        <Twitter />
      </a>
    </SocialCircle>
    <SocialCircle variant={props.variant} color="#1877F2">
      <a
        target="_blank"
        rel="noreferrer noopener"
        href="https://www.facebook.com/pythonitalia/"
      >
        <Facebook />
      </a>
    </SocialCircle>
    <SocialCircle variant={props.variant} color="#FF0076">
      <a
        target="_blank"
        rel="noreferrer noopener"
        href="https://www.instagram.com/python.it/"
      >
        <Instagram />
      </a>
    </SocialCircle>
    <SocialCircle variant={props.variant} color="#2867B2">
      <a
        target="_blank"
        rel="noreferrer noopener"
        href="https://www.linkedin.com/company/pycon-italia/"
      >
        <Linkedin />
      </a>
    </SocialCircle>
  </Flex>
);
