import {
  LayoutContent,
  ScrollDownArrowBar,
  HeroIllustration,
} from "@python-italia/pycon-styleguide";
import React from "react";

import { Landscape } from "./landscape";
import { LandscapeNight } from "./landscape-night";

type Props = {
  cycle: "day" | "night";
};

const Illustration = React.memo(HeroIllustration);

export const HomepageHero = ({ cycle }: Props) => {
  return (
    <div className="h-screen relative mt-[-158px]">
      <div className="h-[calc(100vh-60px)]">
        <Illustration />
      </div>

      <LayoutContent
        showFrom="desktop"
        style={{
          position: "absolute",
          bottom: "-1px",
          width: "100%",
          zIndex: 100,
        }}
      >
        <ScrollDownArrowBar />
      </LayoutContent>
    </div>
  );
};
