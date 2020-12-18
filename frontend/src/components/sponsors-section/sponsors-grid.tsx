/** @jsxRuntime classic */
/** @jsx jsx */
import Image from "next/image";
import { Box, Grid, jsx } from "theme-ui";

import { useSSRResponsiveValue } from "~/helpers/use-ssr-responsive-value";

import { Sponsor } from "./types";

type Props = {
  color?: string | null;
  sponsors: Sponsor[];
};

type ItemProps = {
  color: string;
  sponsor: Sponsor;
};

const SponsorItem: React.FC<ItemProps> = ({ sponsor, color }) => (
  <Box
    sx={{
      backgroundColor: color,
    }}
  >
    <a
      target="_blank"
      href={sponsor.link!}
      sx={{
        filter: "saturate(0)",
        transition: "0.3s filter ease-in-out",
        position: "relative",
        display: "block",
        "> span": {
          display: "block",
        },
        "&:hover": {
          filter: "none",
        },
      }}
    >
      <Box
        sx={{
          display: "inline-block",
          pt: "40%",
        }}
      />

      {sponsor.image && (
        <Box
          sx={{
            position: "absolute",
            top: "40px",
            bottom: "40px",
            left: "40px",
            right: "40px",
          }}
        >
          <Image
            sx={{
              objectFit: "contain",
            }}
            layout="fill"
            src={sponsor.image}
            alt={sponsor.name}
          />
        </Box>
      )}
    </a>
  </Box>
);

export const SponsorsGrid: React.FC<Props> = ({ sponsors, color }) => {
  const columns = useSSRResponsiveValue([1, 3]);
  const missing =
    sponsors.length % columns === 0 ? 0 : columns - (sponsors.length % columns);

  const backgroundColor = color || "yellow";

  return (
    <Grid
      columns={[1, 3]}
      gap={1}
      sx={{
        maxWidth: "container",
        mx: "auto",
        border: "primary",
        background: "black",
      }}
    >
      {sponsors.map((sponsor) => (
        <SponsorItem
          key={sponsor.name}
          sponsor={sponsor}
          color={backgroundColor}
        />
      ))}
      {new Array(missing).fill(null).map((_, index) => (
        <Box
          key={index}
          sx={{
            backgroundColor,
          }}
        />
      ))}
    </Grid>
  );
};
