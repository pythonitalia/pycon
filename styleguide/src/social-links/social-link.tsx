import React from "react";
import { FacebookIcon } from "../icons/facebook";
import { InstagramIcon } from "../icons/instagram";
import { TwitterIcon } from "../icons/twitter";
import { LinkedinIcon } from "../icons/linkedin";
import { Link } from "../link";
import { MastodonIcon } from "../icons/mastodon";
import { Color } from "../types";

export type SocialLinkProps = {
  link: string;
  icon:
    | "twitter"
    | "facebook"
    | "instagram"
    | "youtube"
    | "linkedin"
    | "mastodon";
  rel?: string;
  color?: Color;
  hoverColor?: Color;
};

export const SocialLink = ({ link, icon, rel, color, hoverColor }: SocialLinkProps) => (
  <Link
    color={color}
    hoverColor={hoverColor}
    target="_blank"
    href={link}
    rel={rel}
    className="w-full h-full"
  >
    {icon === "twitter" && <TwitterIcon className="w-full h-full" />}
    {icon === "facebook" && <FacebookIcon className="w-full h-full" />}
    {icon === "instagram" && <InstagramIcon className="w-full h-full" />}
    {icon === "linkedin" && <LinkedinIcon className="w-full h-full" />}
    {icon === "mastodon" && <MastodonIcon className="w-full h-full" />}
  </Link>
);
