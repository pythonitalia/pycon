import {
  Grid,
  Heading,
  Button,
  LayoutContent,
  Section,
  GridColumn,
  Spacer,
  Text,
  SponsorsGrid,
} from "@python-italia/pycon-styleguide";
import React from "react";

import { useCurrentLanguage } from "~/locale/context";
import {
  Cta,
  SponsorsSectionLayout,
  querySponsorsSection,
  useSponsorsSectionQuery,
} from "~/types";

import { createHref } from "../../link";

type Props = {
  title: string;
  body: string;
  layout: SponsorsSectionLayout;
  cta: Cta | null;
};

export const SponsorsSection = ({ title, body, cta }: Props) => {
  const language = useCurrentLanguage();
  const {
    data: { conference },
  } = useSponsorsSectionQuery({
    variables: {
      code: process.env.conferenceCode,
    },
  });
  const sponsorsByLevel = conference.sponsorsByLevel;

  if (sponsorsByLevel.length === 0) {
    return null;
  }

  return (
    <LayoutContent position="relative">
      <Section spacingSize="3xl">
        <Grid cols={12} mdCols={12}>
          <GridColumn colSpan={5} mdColSpan={5}>
            <div className="sticky top-[10px]">
              <Heading size="display2" className="text-center md:text-left">
                {title}
              </Heading>
              <Spacer size="large" />
              <Text
                as="p"
                size={1}
                color="grey-900"
                className="text-center md:text-left"
              >
                {body}
              </Text>
              {cta && (
                <>
                  <Spacer size="large" />
                  <Button
                    href={createHref({
                      path: cta.link,
                      locale: language,
                    })}
                    size="small"
                    role="secondary"
                  >
                    {cta.label}
                  </Button>
                  <Spacer size="large" />
                </>
              )}
            </div>
          </GridColumn>
          <GridColumn mdColStart={7} colStart={7} colSpan={6} mdColSpan={6}>
            <SponsorsGrid
              tiers={sponsorsByLevel.map((tier) => ({
                ...tier,
                cols: getSponsorsPerRow(tier.name),
              }))}
            />
          </GridColumn>
        </Grid>
      </Section>
    </LayoutContent>
  );
};

SponsorsSection.dataFetching = (client) => {
  return [
    querySponsorsSection(client, {
      code: process.env.conferenceCode,
    }),
  ];
};

const getSponsorsPerRow = (level: string) => {
  switch (level) {
    case "Keystone":
    case "Gold":
    case "Silver":
      return 2;
    case "Partners":
    case "Partner":
      return 5;
    default:
      return 3;
  }
};
