import React from "react";
import { SpeakerSquare } from "../speaker-square/speaker-square";
import { Carousel } from "./carousel";

export default {
  title: "Carousel",
};

export const Standard = () => (
  <Carousel title="The speakers">
    <SpeakerSquare
      name="Patrick"
      subtitle="Python Italia"
      portraitUrl="https://source.unsplash.com/900x900/?face&1"
      className="bg-orange"
    />

    <SpeakerSquare
      name="Patrick"
      subtitle="Python Italia"
      portraitUrl="https://source.unsplash.com/900x900/?face&2"
      className="bg-keppel"
    />

    <SpeakerSquare
      name="Patrick"
      subtitle="Python Italia"
      portraitUrl="https://source.unsplash.com/900x900/?face&3"
      className="bg-casablanca"
    />

    <SpeakerSquare
      name="Patrick"
      subtitle="Python Italia"
      portraitUrl="https://source.unsplash.com/900x900/?face&4"
      className="bg-aquamarine"
    />

    <SpeakerSquare
      name="Patrick"
      subtitle="Python Italia"
      portraitUrl="https://source.unsplash.com/900x900/?face&5"
      className="bg-orange"
    />
  </Carousel>
);
