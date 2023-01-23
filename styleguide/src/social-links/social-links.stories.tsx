import React from "react";
import { Spacer } from "../spacer";
import { SocialLinks } from "./social-links";

export default {
  title: "Social links",
};

export const Primary = () => {
  return (
    <div className="p-6">
      <SocialLinks
        socials={[
          {
            icon: "twitter",
            link: "https://twitter.com/pyconit",
          },
          {
            icon: "facebook",
            link: "https://www.facebook.com/pythonitalia",
          },
          {
            icon: "instagram",
            link: "https://www.instagram.com/python.it",
          },
          {
            icon: "linkedin",
            link: "https://www.linkedin.com/company/pycon-italia",
          },
        ]}
      />
      <Spacer size="medium" />

      <div className="bg-black p-6">
        <SocialLinks
          color="milk"
          hoverColor="green"
          socials={[
            {
              icon: "twitter",
              link: "https://twitter.com/pyconit",
            },
            {
              icon: "facebook",
              link: "https://www.facebook.com/pythonitalia",
            },
            {
              icon: "instagram",
              link: "https://www.instagram.com/python.it",
            },
            {
              icon: "linkedin",
              link: "https://www.linkedin.com/company/pycon-italia",
            },
          ]}
        />
      </div>
    </div>
  );
};
