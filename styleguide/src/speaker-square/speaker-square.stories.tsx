import React from "react";

import { SpeakerSquare } from "./speaker-square";

export default {
  title: "Speaker Square",
};

const Template = (args: any) => <SpeakerSquare {...args} />;

export const Primary = Template.bind({});

Primary.args = {
  name: "Patrick",
  subtitle: "Python Italia",
  portraitUrl: "https://source.unsplash.com/900x900/?face",
};
