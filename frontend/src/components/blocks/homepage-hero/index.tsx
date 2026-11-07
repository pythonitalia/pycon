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
import { useCurrentLanguage } from "~/locale/context";
import { type Cta, HomepageHeroCity, HomepageHeroVariant } from "~/types";
import { createHref } from "../../link";

type Props = {
  cycle: "day" | "night";
  city: HomepageHeroCity;
  variant: HomepageHeroVariant;
  title: string;
  subtitle: string;
  body: string;
  highlight: string;
  primaryCta: Cta | null;
  secondaryCta: Cta | null;
};

const HeroIllustrationFlorenceMemo = React.memo(HeroIllustration);
const HeroIllustrationBolognaMemo = React.memo(HeroIllustrationBologna);

export const HomepageHero = ({
  cycle,
  city,
  variant,
  title,
  subtitle,
  body,
  highlight,
  primaryCta,
  secondaryCta,
}: Props) => {
  const isOverlay = variant === HomepageHeroVariant.Overlay;

  return (
    <div className="h-screen relative -mt-[161px] -mb-[3px]">
      <div className="h-screen lg:h-[calc(100vh-60px)]">
        {city === HomepageHeroCity.Florence && (
          <HeroIllustrationFlorenceMemo cycle={cycle} />
        )}
        {city === HomepageHeroCity.Bologna && (
          <HeroIllustrationBolognaMemo cycle={cycle} />
        )}
      </div>

      {isOverlay && (
        <HeroOverlay
          title={title}
          subtitle={subtitle}
          body={body}
          highlight={highlight}
          primaryCta={primaryCta}
          secondaryCta={secondaryCta}
        />
      )}

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

type OverlayProps = Pick<
  Props,
  "title" | "subtitle" | "body" | "highlight" | "primaryCta" | "secondaryCta"
>;

const HeroOverlay = ({
  title,
  subtitle,
  body,
  highlight,
  primaryCta,
  secondaryCta,
}: OverlayProps) => (
  // The whole overlay ignores pointer events so the illustration keeps its
  // easter egg (clicking the church swaps day and night), only the CTAs take
  // clicks back.
  <div className="absolute inset-0 z-40 pointer-events-none">
    <Scrim />

    <div className="relative h-full flex flex-col justify-center pt-[161px] pb-16 lg:pb-32">
      <Container>
        <div className="max-w-[600px]">
          {title && (
            <Heading size="display2" color="milk">
              {title}
            </Heading>
          )}
          {subtitle && (
            <>
              <Spacer size="small" />
              <Heading size={2} color="milk">
                {subtitle}
              </Heading>
            </>
          )}
          {body && (
            <>
              <Spacer size="medium" />
              <Text as="p" size={1} color="milk">
                {body}
              </Text>
            </>
          )}
          {(primaryCta || secondaryCta) && (
            <>
              <Spacer size="large" />
              <div className="flex flex-col md:flex-row md:items-center gap-4 md:gap-6 pointer-events-auto">
                {primaryCta && <HeroCta cta={primaryCta} background="coral" />}
                {secondaryCta && (
                  <HeroCta cta={secondaryCta} variant="secondary" />
                )}
              </div>
            </>
          )}
          {highlight && (
            <>
              <Spacer size="medium" />
              <Text as="p" size="label3" weight="strong" uppercase color="milk">
                {highlight}
              </Text>
            </>
          )}
        </div>
      </Container>
    </div>
  </div>
);

/**
 * The hero illustration cannot carry light text on its own: the day sky is a
 * mid-tone periwinkle (#6A80EF) that only reaches 3.3:1 against milk, and the
 * bottom half is crowded with hills, the church, the two towers and the snake.
 *
 * The vertical scrim carries mobile, where the copy spans the full width. On
 * desktop it is lightened and paired with a horizontal one so the copy column
 * on the left is the only part that gets darkened, leaving the landmarks on the
 * right side of the frame readable. Combined, the copy area sits at ~0.55-0.75
 * black over the artwork, which is >=8:1 against milk in both cycles.
 */
const Scrim = () => (
  <>
    <div className="absolute inset-0 bg-gradient-to-b from-black/80 via-black/60 to-transparent lg:from-black/65 lg:via-black/25" />
    <div className="hidden lg:block absolute inset-0 bg-gradient-to-r from-black/70 via-black/40 to-transparent" />
  </>
);

const HeroCta = ({
  cta,
  ...buttonProps
}: {
  cta: Cta;
} & Pick<React.ComponentProps<typeof Button>, "variant" | "background">) => {
  const language = useCurrentLanguage();
  const setCurrentModal = useSetCurrentModal();
  const isModalCta = cta.link?.startsWith("modal:");

  const openModal = (e) => {
    if (!isModalCta) {
      return;
    }

    e.preventDefault();
    setCurrentModal(cta.link.replace("modal:", "") as ModalID);
  };

  return (
    <Button
      {...buttonProps}
      fullWidth="mobile"
      onClick={openModal}
      href={
        isModalCta
          ? undefined
          : createHref({ path: cta.link, locale: language })
      }
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
