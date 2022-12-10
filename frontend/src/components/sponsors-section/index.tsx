/** @jsxRuntime classic */

/** @jsx jsx */
import { Heading, Spacer } from "@python-italia/pycon-styleguide";
import { jsx } from "theme-ui";

import { SponsorsGrid } from "./sponsors-grid";
import { Sponsor } from "./types";

type Props = {
  sponsorsByLevel: {
    level: string;
    sponsors: Sponsor[];
    highlightColor?: string | null;
  }[];
  sx?: any;
};

export const SponsorsSection = ({ sponsorsByLevel, ...props }: Props) => (
  <div {...props}>
    {sponsorsByLevel.map(({ level, sponsors, highlightColor }, index) => (
      <div key={level}>
        <Heading size={2}>{level}</Heading>
        <Spacer size="xs" />
        <SponsorsGrid color={highlightColor} sponsors={sponsors} />
        {index !== sponsorsByLevel.length - 1 && <Spacer size="large" />}
      </div>
    ))}
  </div>
);
