import React from "react";
import { Logo } from "../logo/logo";
import { Footer } from "./footer";

export default {
  title: "Footer",
};

export const Standard = () => (
  <div className="pt-24">
    <Footer
      logo={Logo}
      socials={[
        { link: "#", icon: "twitter" },
        { link: "#", icon: "facebook" },
        { link: "#", icon: "instagram" },
        { link: "#", icon: "linkedin" },
        { link: "#", icon: "mastodon" },
      ]}
      bottomLinks={[
        {
          link: "#",
          text: "Code of Conduct",
        },
        {
          link: "#",
          text: "Code of Conduct 2",
        },
        {
          link: "#",
          text: "Code of Conduct 3",
        },
      ]}
    />
  </div>
);
