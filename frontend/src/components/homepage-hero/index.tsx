import {
  LayoutContent,
  ScrollDownArrowBar,
} from "@python-italia/pycon-styleguide";
import React from "react";

import { Landscape } from "./landscape";
import { LandscapeNight } from "./landscape-night";

type Props = {
  cycle: "day" | "night";
};

export const HomepageHero = ({ cycle }: Props) => {
  const Illustration = cycle === "day" ? Landscape : LandscapeNight;
  return (
    <div
      style={{
        marginTop: -158,
        position: "relative",
      }}
    >
      <Illustration
        style={{
          left: 0,
          top: 0,
          height: "100vh",
          width: "100%",
        }}
      />

      <LayoutContent
        showFrom="desktop"
        style={{ position: "absolute", bottom: "-1px", width: "100%" }}
      >
        <ScrollDownArrowBar />
      </LayoutContent>
    </div>
  );
};
