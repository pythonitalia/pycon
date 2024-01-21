import {
  LayoutContent,
  ScrollDownArrowBar,
  HeroIllustration,
} from "@python-italia/pycon-styleguide";
import React from "react";

type Props = {
  cycle: "day" | "night";
};

const Illustration = React.memo(HeroIllustration);

export const HomepageHero = ({ cycle }: Props) => {
  return (
    <div className="h-screen relative -mt-[161px]">
      <div className="h-screen lg:h-[calc(100vh-60px)]">
        <Illustration cycle={cycle} />
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
