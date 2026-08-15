import {
  Button,
  Container,
  Heading,
  HeroIllustration,
  HeroIllustrationBologna,
  LayoutContent,
  ScrollDownArrowBar,
  Spacer,
  Text,
} from "@python-italia/pycon-styleguide";
import React from "react";
import { type ModalID, useSetCurrentModal } from "~/components/modal/context";
import { type Cta, HomepageHeroCity } from "~/types";

type Props = {
  cycle: "day" | "night";
  city: HomepageHeroCity;
  title: string;
  location: string;
  dates: string;
  subtitle: string;
  highlight: string;
  primaryCta: Cta | null;
  secondaryCta: Cta | null;
};

const HeroIllustrationFlorenceMemo = React.memo(HeroIllustration);
const HeroIllustrationBolognaMemo = React.memo(HeroIllustrationBologna);

const Illustration = ({ cycle, city }: Pick<Props, "cycle" | "city">) => (
  <>
    {city === HomepageHeroCity.Florence && (
      <HeroIllustrationFlorenceMemo cycle={cycle} />
    )}
    {city === HomepageHeroCity.Bologna && (
      <HeroIllustrationBolognaMemo cycle={cycle} />
    )}
  </>
);

const HeroCTA = ({
  cta,
  variant,
}: {
  cta: Cta;
  variant: "primary" | "secondary";
}) => {
  const setCurrentModal = useSetCurrentModal();
  const isModalCTA = cta.link?.startsWith("modal:");
  const openModal = (e) => {
    if (!isModalCTA) {
      return;
    }
    e.preventDefault();

    setCurrentModal(cta.link.replace("modal:", "") as ModalID);
  };

  return (
    <Button
      onClick={openModal}
      href={isModalCTA ? null : cta.link}
      variant={variant}
      fullWidth="mobile"
    >
      {cta.label}
    </Button>
  );
};

export const HomepageHero = ({
  cycle,
  city,
  title,
  location,
  dates,
  subtitle,
  highlight,
  primaryCta,
  secondaryCta,
}: Props) => {
  const hasCopy = Boolean(
    title || location || dates || subtitle || primaryCta || secondaryCta,
  );

  // Pages that only configure the city keep the original full-bleed
  // illustration, so this block stays valid until the copy is filled in.
  if (!hasCopy) {
    return (
      <div className="h-screen relative -mt-[161px] -mb-[3px]">
        <div className="h-screen lg:h-[calc(100vh-60px)]">
          <Illustration cycle={cycle} city={city} />
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
  }

  const whenAndWhere = [location, dates].filter(Boolean).join(" · ");

  return (
    <div className="overflow-clip">
      <Container className="grid grid-cols-1 lg:grid-cols-2 lg:gap-10">
        <div className="flex flex-col justify-center py-12 lg:py-20 lg:min-h-[34rem]">
          {whenAndWhere && (
            <>
              <Text uppercase size={1} weight="strong">
                {whenAndWhere}
              </Text>
              <Spacer size="small" />
            </>
          )}

          {title && <Heading size="display1">{title}</Heading>}

          {subtitle && (
            <>
              <Spacer size="medium" />
              <Heading size={2}>{subtitle}</Heading>
            </>
          )}

          {(primaryCta || secondaryCta) && (
            <>
              <Spacer size="large" />
              <div className="flex flex-col md:flex-row gap-4">
                {primaryCta && <HeroCTA cta={primaryCta} variant="primary" />}
                {secondaryCta && (
                  <HeroCTA cta={secondaryCta} variant="secondary" />
                )}
              </div>
            </>
          )}

          {highlight && (
            <>
              <Spacer size="medium" />
              <Text size={2} weight="strong">
                {highlight}
              </Text>
            </>
          )}
        </div>

        <div className="relative w-screen -ml-4 h-64 md:h-80 lg:w-full-outside-container lg:ml-0 lg:h-auto lg:border-l-3">
          {/* the illustration fills the column, whose height comes from the copy */}
          <div className="absolute inset-0">
            <Illustration cycle={cycle} city={city} />
          </div>
        </div>
      </Container>
    </div>
  );
};

HomepageHero.getStaticProps = () => {
  const utcHours = new Date().getUTCHours();
  const cycle = utcHours > 5 && utcHours < 17 ? "day" : "night";

  return { cycle };
};
