import React from "react";
import { Header } from "../header/header";
import { SplitSection } from "../split-section/split-section";
import { Marquee } from "../marquee/marquee";
import { Page } from "./page";
import { Carousel } from "../carousel/carousel";

export default {
  title: "Page examples",
};

export const Standard = () => (
  <div>
    <Page>
      <Header />
      <Marquee>Style guides rock 🚀</Marquee>
      <SplitSection title="The speakers">
        <p className="font-bold text-purple-600 mb-8">
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
        <div className="bg-red-400"></div>
        <div className="bg-blue-400"></div>
        <div className="bg-purple-400"></div>
        <div className="bg-yellow-400"></div>
        <div className="bg-red-400"></div>
        <div className="bg-blue-400"></div>
        <div className="bg-purple-400"></div>
        <div className="bg-yellow-400"></div>
      </Carousel>
    </Page>
  </div>
);
