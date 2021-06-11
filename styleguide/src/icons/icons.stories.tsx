import React from "react";
import { FacebookIcon } from "./facebook";
import { GithubIcon } from "./github";
import { InstagramIcon } from "./instagram";
import { TwitterIcon } from "./twitter";

export default {
  title: "Icons",
};

const Template = ({ component: Component }) => {
  return (
    <>
      <Component width={14} height={14} />
      <Component width={28} height={28} />
      <Component width={42} height={42} />
      <Component width={64} height={64} />
      <Component width={128} height={128} />
    </>
  );
};
Template.args = { component: GithubIcon };

export const Github = Template.bind({});
Github.args = { component: GithubIcon };

export const Twitter = Template.bind({});
Twitter.args = { component: TwitterIcon };

export const Instagram = Template.bind({});
Instagram.args = { component: InstagramIcon };

export const Facebook = Template.bind({});
Facebook.args = { component: FacebookIcon };
