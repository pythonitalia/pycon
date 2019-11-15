/** @jsx jsx */
import css from "@styled-system/css";
import { Box, Grid, Heading } from "@theme-ui/components";
import Img from "gatsby-image";
import { jsx } from "theme-ui";

import { HomePageQuery } from "../../generated/graphql";
import { Link } from "../link";

type Props = {
  sponsors: HomePageQuery["backend"]["conference"]["sponsorsByLevel"][0]["sponsors"];
};

const SponsorItem: React.SFC<{ sponsor: Props["sponsors"][0] }> = ({
  sponsor,
}) => (
  <Box
    sx={{
      backgroundColor: "yellow",
    }}
  >
    <Link
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

export const SponsorsGrid: React.SFC<Props> = ({ sponsors }) => {
  const columns = 3;
  const missing = columns - (sponsors.length % columns);

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
        <SponsorItem key={sponsor.name} sponsor={sponsor} />
      ))}
      {new Array(missing).fill(null).map((_, index) => (
        <Box
          key={index}
          sx={{
            backgroundColor: "yellow",
          }}
        />
      ))}
    </Grid>
  );
};
