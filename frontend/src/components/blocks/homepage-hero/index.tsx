import {
  Button,
  Container,
  Grid,
  GridColumn,
  Heading,
  HeroIllustration,
  HeroIllustrationBologna,
  LayoutContent,
  ScrollDownArrowBar,
  Spacer,
  Text,
} from "@python-italia/pycon-styleguide";
import type { Illustration } from "@python-italia/pycon-styleguide/dist/illustrations/types";
import { getIllustration } from "@python-italia/pycon-styleguide/illustrations";
import React from "react";
import { type Cta, HomepageHeroCity } from "~/types";
import { type ModalID, useSetCurrentModal } from "../../modal/context";

type Props = {
  cycle: "day" | "night";
  city: HomepageHeroCity | null;
  pretitle: string;
  title: string;
  subtitle: string;
  highlight: string;
  illustration: string;
  primaryCta: Cta | null;
  secondaryCta: Cta | null;
};

const HeroIllustrationFlorenceMemo = React.memo(HeroIllustration);
const HeroIllustrationBolognaMemo = React.memo(HeroIllustrationBologna);

const CityIllustration = ({ city, cycle }: Pick<Props, "city" | "cycle">) => (
  <>
    {city === HomepageHeroCity.Florence && (
      <HeroIllustrationFlorenceMemo cycle={cycle} />
    )}
    {city === HomepageHeroCity.Bologna && (
      <HeroIllustrationBolognaMemo cycle={cycle} />
    )}
  </>
);

export const HomepageHero = ({
  cycle,
  city,
  pretitle,
  title,
  subtitle,
  highlight,
  illustration,
  primaryCta,
  secondaryCta,
}: Props) => {
  const hasCopy = !!(title || pretitle || subtitle || primaryCta);

  if (!hasCopy) {
    return <FullScreenHero cycle={cycle} city={city} />;
  }

  return (
    <SplitHero
      cycle={cycle}
      city={city}
      pretitle={pretitle}
      title={title}
      subtitle={subtitle}
      highlight={highlight}
      illustration={illustration}
      primaryCta={primaryCta}
      secondaryCta={secondaryCta}
    />
  );
};

const FullScreenHero = ({ cycle, city }: Pick<Props, "city" | "cycle">) => {
  return (
    <div className="h-screen relative -mt-[161px] -mb-[3px]">
      <div className="h-screen lg:h-[calc(100vh-60px)]">
        <CityIllustration city={city} cycle={cycle} />
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

const SplitHero = ({
  cycle,
  city,
  pretitle,
  title,
  subtitle,
  highlight,
  illustration,
  primaryCta,
  secondaryCta,
}: Props) => {
  const StaticIllustration = illustration
    ? getIllustration(illustration as Illustration)
    : null;
  const hasIllustration = !!StaticIllustration || !!city;

  return (
    <Container>
      <Spacer size="xl" />
      <Grid cols={12} mdCols={12} alignItems="center">
        <GridColumn colSpan={hasIllustration ? 6 : 12} mdColSpan={12}>
          {pretitle && (
            <>
              <Text uppercase size={1} weight="strong" as="p">
                {pretitle}
              </Text>
              <Spacer size="small" />
            </>
          )}

          {title && <Heading size="display1">{title}</Heading>}

          {subtitle && (
            <>
              <Spacer size="medium" />
              <Text size={1} as="p">
                {subtitle}
              </Text>
            </>
          )}

          {(primaryCta || secondaryCta) && (
            <>
              <Spacer size="large" />
              <div className="flex flex-col md:flex-row md:items-center gap-4">
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
              <Text size={2} weight="strong" as="p">
                {highlight}
              </Text>
            </>
          )}
        </GridColumn>

        {hasIllustration && (
          <GridColumn colSpan={6} mdColSpan={12}>
            {StaticIllustration ? (
              <div className="max-w-[360px] lg:max-w-[488px] w-full mx-auto lg:mr-0">
                <StaticIllustration className="w-full h-full" />
              </div>
            ) : (
              <ScaledCityIllustration city={city} cycle={cycle} />
            )}
          </GridColumn>
        )}
      </Grid>
      <Spacer size="xl" />
    </Container>
  );
};

// The city illustrations are scenes drawn for a full viewport: scale the whole
// scene down instead of cropping it, so nothing (the towers, the snake) is lost
// when it only gets half of the screen.
const ILLUSTRATION_WIDTH = 1440;
const ILLUSTRATION_HEIGHT = 900;

const ScaledCityIllustration = ({
  city,
  cycle,
}: Pick<Props, "city" | "cycle">) => {
  const containerRef = React.useRef<HTMLDivElement>(null);
  const [scale, setScale] = React.useState(0);

  React.useEffect(() => {
    const container = containerRef.current;
    if (!container) {
      return;
    }

    const observer = new ResizeObserver(([entry]) => {
      setScale(entry.contentRect.width / ILLUSTRATION_WIDTH);
    });
    observer.observe(container);
    return () => observer.disconnect();
  }, []);

  return (
    <div
      ref={containerRef}
      className="relative w-full aspect-[16/10] overflow-hidden border-3 border-black bg-black"
    >
      <div
        className="absolute top-0 left-0 origin-top-left"
        style={{
          width: ILLUSTRATION_WIDTH,
          height: ILLUSTRATION_HEIGHT,
          transform: `scale(${scale})`,
        }}
      >
        <CityIllustration city={city} cycle={cycle} />
      </div>
    </div>
  );
};

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

    const modalId = cta.link.replace("modal:", "") as ModalID;
    setCurrentModal(modalId);
  };

  return (
    <Button
      variant={variant}
      onClick={openModal}
      href={isModalCTA ? null : cta.link}
      fullWidth="mobile"
    >
      {cta.label}
    </Button>
  );
};

HomepageHero.getStaticProps = () => {
  const utcHours = new Date().getUTCHours();
  const cycle = utcHours > 5 && utcHours < 17 ? "day" : "night";

  return { cycle };
};
