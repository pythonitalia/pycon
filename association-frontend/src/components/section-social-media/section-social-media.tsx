import React from "react";

import DiscordIcon from "../icons/discord";
import FacebookIcon from "../icons/facebook";
import GitHubIcon from "../icons/github";
import InstagramIcon from "../icons/instagram";
import LinkedInIcon from "../icons/linkedin";
import MailIcon from "../icons/mail";
import TwitterIcon from "../icons/twitter";
import SectionItem from "../section-item/section-item";
import SocialCard from "../social-card/social-card";

const icons = [
  <DiscordIcon />,
  <FacebookIcon />,
  <GitHubIcon />,
  <InstagramIcon />,
  <LinkedInIcon />,
  <TwitterIcon />,
  <MailIcon />,
];

const SectionSocialMedia = () => {
  return (
    <SectionItem title={"Seguici Online 🎭"}>
      <div className="flex flex-row space-x-4 w-full  justify-center">
        {icons.map((icon) => {
          return (
            <div className="flex-shrink-0">
              {" "}
              <SocialCard component={icon} />
            </div>
          );
        })}
      </div>
    </SectionItem>
  );
};
export default SectionSocialMedia;
