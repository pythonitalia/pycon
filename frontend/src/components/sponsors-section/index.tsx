import { SponsorsGrid } from "@python-italia/pycon-styleguide";
import React from "react";

import { IndexPageQueryResult } from "~/types";

type Props = {
  sponsorsByLevel: IndexPageQueryResult["data"]["conference"]["sponsorsByLevel"];
  sx?: any;
};

export const SponsorsSection = ({ sponsorsByLevel }: Props) => (
  <SponsorsGrid
    tiers={sponsorsByLevel.map((tier) => ({
      ...tier,
      cols: getSponsorsPerRow(tier.name),
    }))}
  />
);

const getSponsorsPerRow = (level: string) => {
  switch (level) {
    case "Keystone":
    case "Gold":
    case "Silver":
      return 2;
    case "Partners":
      return 4;
    default:
      return 3;
  }
};
