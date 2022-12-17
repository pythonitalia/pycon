import React from "react";
import { FacebookIcon } from "../icons/facebook";
import { InstagramIcon } from "../icons/instagram";
import { TwitterIcon } from "../icons/twitter";
import { LinkedinIcon } from "../icons/linkedin";
import { Link } from "../link";
import { MastodonIcon } from "../icons/mastodon";

export type SocialLinkProps = {
  link: string;
  icon:
    | "twitter"
    | "facebook"
    | "instagram"
    | "youtube"
    | "linkedin"
    | "mastodon";
};

export const SocialLink = ({ link, icon }: SocialLinkProps) => (
  <Link target="_blank" href={link} rel="me">
    {icon === "twitter" && <TwitterIcon />}
    {icon === "facebook" && <FacebookIcon />}
    {icon === "instagram" && <InstagramIcon />}
    {icon === "linkedin" && <LinkedinIcon />}
    {icon === "mastodon" && <MastodonIcon />}
  </Link>
);
