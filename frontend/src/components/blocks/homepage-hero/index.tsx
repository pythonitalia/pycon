import {
  HeroIllustration,
  LayoutContent,
  ScrollDownArrowBar,
} from "@python-italia/pycon-styleguide";
import React from "react";
import { HomepageHeroCity } from "~/types";

type Props = {
  cycle: "day" | "night";
  city: HomepageHeroCity;
};

const Illustration = React.memo(HeroIllustration);

export const HomepageHero = ({ cycle, city }: Props) => {
  return (
    <div className="h-screen relative -mt-[161px] -mb-[3px]">
      <div className="h-screen lg:h-[calc(100vh-60px)]">
        {city === HomepageHeroCity.Florence && <Illustration cycle={cycle} />}
        {city === HomepageHeroCity.Bologna && <div>Bologna illustration</div>}
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

HomepageHero.getStaticProps = () => {
  const utcHours = new Date().getUTCHours();
  const cycle = utcHours > 5 && utcHours < 17 ? "day" : "night";

  return { cycle };
};
