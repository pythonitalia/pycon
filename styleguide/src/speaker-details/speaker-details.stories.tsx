import React from "react";

import { SpeakerDetails } from "./speaker-details";

export default {
  title: "Speaker details",
};

export const Primary = () => (
  <div>
    <SpeakerDetails
      name="Matteo Benci"
      website="http://google.com"
      twitter="google"
      occupation="best person ever"
      portraitUrl="https://pbs.twimg.com/profile_images/1380076828921098247/9vosOQ1U.jpg"
      bio="best person ever"
    />
  </div>
);
