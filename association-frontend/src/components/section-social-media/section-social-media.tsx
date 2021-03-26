import React from "react";

import DiscordIcon from "~/components/icons/discord";
import FacebookIcon from "~/components/icons/facebook";
import GitHubIcon from "~/components/icons/github";
import InstagramIcon from "~/components/icons/instagram";
import LinkedInIcon from "~/components/icons/linkedin";
import MailIcon from "~/components/icons/mail";
import TwitterIcon from "~/components/icons/twitter";
import SectionItem from "~/components/section-item/section-item";
import SocialCard from "~/components/social-card/social-card";

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
