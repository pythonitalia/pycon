import React from "react";
import { Heading } from "../heading";
import { Grid } from "../grid";
import { Spacer } from "../spacer";
import clsx from "clsx";

type Sponsor = {
  name: string;
  logo: string;
  url: string;
};

type SponsorsTier = {
  name: string;
  cols?: number;
  sponsors: Sponsor[];
};

type Props = {
  tiers: SponsorsTier[];
};

const getClassNames = (cols: number) => {
  switch (cols) {
    case 1:
      return "lg:w-[70%]";
    default:
      return "";
  }
}

export const SponsorsGrid = ({ tiers }: Props) => {
  return (
    <div>
      {tiers.map((tier, index) => {
        const cols = tier.cols ?? 2;
        const classNames = getClassNames(cols);

        return (
          <div key={tier.name}>
            <Heading size={2}>{tier.name}</Heading>
            <Spacer size="xs" />
            <Grid gap="small" cols={cols} mdCols={Math.ceil(cols / 2)} className={classNames}>
              {tier.sponsors.map((sponsor) => (
                <SponsorItem sponsor={sponsor} key={sponsor.name} cols={cols} />
              ))}
            </Grid>
            {index !== tiers.length - 1 && <Spacer size="large" />}
          </div>
        );
      })}
    </div>
  );
};

const getInset = (cols: number) => {
  switch (cols) {
    case 1:
      return "inset-0 md:inset-2";
    case 2:
      return "inset-10 lg:inset-6";
    default:
      return "inset-10 md:inset-4 lg:inset-2";
  }
};

const getPaddings = (cols: number) => {
  switch (cols) {
    case 1:
      return "pb-[50%] lg:pb-[50%]";
    default:
      return "pb-[50%] lg:pb-[60%]";
  }
}

const SponsorItem = ({ sponsor, cols }: { sponsor: Sponsor; cols: number }) => {
  const inset = getInset(cols);
  const paddings = getPaddings(cols);

  return (
    <a
      className="bg-cream border border-black relative"
      href={sponsor.url}
      target="_blank"
      rel="noopener"
    >
      <div>
        <div className={paddings}></div>

        <div className={clsx("absolute", inset)}>
          <img
            src={sponsor.logo}
            alt={sponsor.name}
            loading="lazy"
            className="w-full h-full object-contain"
          />
        </div>
      </div>
    </a>
  );
};
