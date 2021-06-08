import React from "react";
import { Header } from "../header/header";
import { SplitSection } from "../split-section/split-section";
import { Marquee } from "../marquee/marquee";
import { Page } from "./page";
import { Carousel } from "../carousel/carousel";
import { SpeakerSquare } from "../speaker-square/speaker-square";
import { EmbeddedTwitch } from "../embedded-video";

export default {
  title: "Page examples",
};

export const Standard = () => (
  <div>
    <Page>
      <Header />
      <Marquee>Style guides rock 🚀</Marquee>
      <EmbeddedTwitch channel={"landonorris"} width={620} height={378}></EmbeddedTwitch>


      <SplitSection title="The speakers">
        <p className="mb-8 font-bold text-purple-600">
          Lorem ipsum dolor sit, amet consectetur adipisicing elit.
        </p>
        <p>
          Lorem ipsum dolor sit, amet consectetur adipisicing elit. Eius
          delectus velit temporibus facilis quis dolore sit fugit vel labore, ut
          odit perspiciatis id, vitae maiores? Sequi cupiditate soluta officia
          voluptatem?
        </p>
      </SplitSection>
      <Carousel title="The speakers">
        <SpeakerSquare
          name="Patrick"
          subtitle="Python Italia"
          portraitUrl="https://source.unsplash.com/900x900/?face&1"
          className="bg-red-400"
        />

        <SpeakerSquare
          name="Patrick"
          subtitle="Python Italia"
          portraitUrl="https://source.unsplash.com/900x900/?face&2"
          className="bg-blue-400"
        />

        <SpeakerSquare
          name="Patrick"
          subtitle="Python Italia"
          portraitUrl="https://source.unsplash.com/900x900/?face&3"
          className="bg-purple-400"
        />

        <SpeakerSquare
          name="Patrick"
          subtitle="Python Italia"
          portraitUrl="https://source.unsplash.com/900x900/?face&4"
          className="bg-yellow-400"
        />

        <SpeakerSquare
          name="Patrick"
          subtitle="Python Italia"
          portraitUrl="https://source.unsplash.com/900x900/?face&5"
          className="bg-red-400"
        />
      </Carousel>
    </Page>
  </div>
);
