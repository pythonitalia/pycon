/** @jsx jsx */
import { Box, Grid } from "@theme-ui/components";
import Img from "gatsby-image";
import { jsx } from "theme-ui";

import { HomePageQuery } from "../../generated/graphql";
import { Link } from "../link";

type Props = {
  color?: string | null;
  sponsors: HomePageQuery["backend"]["conference"]["sponsorsByLevel"][0]["sponsors"];
};

type ItemProps = {
  color: string;
  sponsor: Props["sponsors"][0];
};

const SponsorItem: React.SFC<ItemProps> = ({ sponsor, color }) => (
  <Box
    sx={{
      backgroundColor: color,
    }}
  >
    <Link
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

      <Img
        style={{
          position: "absolute",
          top: 0,
          bottom: 0,
          left: 0,
          right: 0,
        }}
        imgStyle={{
          objectFit: "contain",
        }}
        alt={sponsor.name}
        {...sponsor.imageFile!.childImageSharp}
      />
    </Link>
  </Box>
);

export const SponsorsGrid: React.SFC<Props> = ({ sponsors, color }) => {
  const columns = 3;
  const missing = columns - (sponsors.length % columns);

  const backgroundColor = color || "yellow";

  return (
    <Grid
      columns={columns}
      gap={1}
      sx={{
        maxWidth: "container",
        mx: "auto",
        border: "primary",
        background: "black",
      }}
    >
      {sponsors.map(sponsor => (
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
