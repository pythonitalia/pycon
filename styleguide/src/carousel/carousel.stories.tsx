import React from "react";
import { SpeakerSquare } from "../speaker-square/speaker-square";
import { Carousel } from "./carousel";

export default {
  title: "Carousel",
};

export const Standard = ({ items }) => (
  <Carousel title="The speakers">
    {new Array(items).fill(null).map((_, index) => (
      <SpeakerSquare
        key={index}
        name={`Speaker ${index + 1}`}
        subtitle="Python Italia"
        portraitUrl={`https://source.unsplash.com/800x800/?face&${index}`}
        className="bg-coral"
      />
    ))}
  </Carousel>
);

Standard.args = {
  items: 10,
};
