import React from "react";
import { HeroIllustrationBologna } from "./hero-illustration-bologna";

export default {
  title: "Hero Illustration Bologna",
};

export const Day = () => {
  return (
    <div className="h-screen w-screen">
      <HeroIllustrationBologna cycle="day" />
    </div>
  );
};

export const Night = () => {
  return (
    <div className="h-screen w-screen">
      <HeroIllustrationBologna cycle="night" />
    </div>
  );
};
