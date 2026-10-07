import React from "react";
import { Grid } from "../grid";

import { SpeakerCard } from "./speaker-card";

export default {
  title: "Speaker Card",
  argTypes: {
    talkTitle: {
      defaultValue: "Talk title",
      control: {
        type: "text",
      },
    },
    portraitUrl: {
      defaultValue: "https://source.unsplash.com/900x900/?face",
      control: {
        type: "text",
      },
    },
    speakerName: {
      defaultValue: "Speaker name",
      control: {
        type: "text",
      },
    },
  },
};

export const Primary = (args: any) => <SpeakerCard {...args} />;

export const MultipleCards = (args: any) => {
  return (
    <Grid cols={3}>
      <SpeakerCard
        talkInfoLeft="27 July"
        talkInfoRight="English, Lemon"
        {...args}
      />
      <SpeakerCard
        {...args}
        talkInfoLeft="Left"
        talkTitle="Longer talk title Longer talk title Longer talk title Longer talk title "
      />
      <SpeakerCard {...args} talkInfoRight="Right" />
      <SpeakerCard {...args} />
      <SpeakerCard {...args} />
      <SpeakerCard {...args} />
    </Grid>
  );
};
