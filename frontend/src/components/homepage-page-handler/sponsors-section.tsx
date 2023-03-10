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
import { FormattedMessage } from "react-intl";

import { IndexPageQuery } from "~/types";

type Props = {
  sponsorsByLevel: IndexPageQuery["conference"]["sponsorsByLevel"];
};

export const SponsorsSection = ({ sponsorsByLevel }: Props) => {
  if (sponsorsByLevel.length === 0) {
    return null;
  }

  return (
    <LayoutContent position="relative">
      <Section spacingSize="3xl">
        <Grid cols={12} mdCols={12}>
          <GridColumn colSpan={5} mdColSpan={5}>
            <LayoutContent position="sticky" style={{ top: 10 }}>
              <Heading size="display2">Sponsors</Heading>
              <Spacer size="large" />
              <Text size={1} color="grey-900">
                <FormattedMessage id="homepage.sponsorsSectionText" />
              </Text>
              <Spacer size="large" />
              <Button href="/sponsor" size="small" role="secondary">
                <FormattedMessage id="homepage.sponsorsSectionCTAText" />
              </Button>
            </LayoutContent>
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

const getSponsorsPerRow = (level: string) => {
  switch (level) {
    case "Keystone":
    case "Gold":
    case "Silver":
      return 2;
    case "Partners":
    case "Partner":
      return 4;
    default:
      return 3;
  }
};
