import React from "react";
import { SpeakerSquare } from "../speaker-square/speaker-square";
import { Carousel } from "./carousel";

export default {
  title: "Carousel",
};

export const Standard = () => (
  <Carousel title="The speakers">
    {new Array(10).fill(null).map((_, index) => (
      <SpeakerSquare
        key={index}
        name={`Speaker ${index + 1}`}
        subtitle="Python Italia"
        portraitUrl={`https://source.unsplash.com/800x800/?face&${index}`}
        className="bg-orange"
      />
    ))}
  </Carousel>
);
