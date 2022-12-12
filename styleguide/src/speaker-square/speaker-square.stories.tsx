import React from "react";

import { SpeakerSquare } from "./speaker-square";

export default {
  title: "Speaker Square",
};

const Template = (args: any) => (
  <SpeakerSquare
    {...args}
    linkWrapper={args.url ? <a href={args.url} /> : null}
  />
);

export const Primary = Template.bind({});

// @ts-ignore
Primary.args = {
  name: "Patrick",
  subtitle: "Python Italia",
  portraitUrl: "https://source.unsplash.com/900x900/?face",
  url: "",
};
