import React from "react";
import { HeroIllustration } from "./hero-illustration";

export default {
  title: "Hero Illustration",
};

export const Primary = () => {
  return (
    <div className="h-screen w-screen">
      <HeroIllustration cycle="day" />
    </div>
  );
};

export const Night = () => {
  return (
    <div className="h-screen w-screen">
      <HeroIllustration cycle="night" />
    </div>
  );
};
