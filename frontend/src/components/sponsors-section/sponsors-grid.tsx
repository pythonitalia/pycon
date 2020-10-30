/** @jsxRuntime classic */
/** @jsx jsx */
import LazyLoad from "react-lazyload";
import { Box, Grid, jsx } from "theme-ui";

import { useSSRResponsiveValue } from "~/helpers/use-ssr-responsive-value";

import { Link } from "../link";
import { Sponsor } from "./types";

type Props = {
  color?: string | null;
  sponsors: Sponsor[];
};

type ItemProps = {
  color: string;
  sponsor: Sponsor;
};

const getImageUrl = (url: string) => {
  const newUrl = url.replace(
    "https://production-pycon-backend-media.s3.amazonaws.com",
    "https://pycon.imgix.net",
  );
  const parts = newUrl.split("?");
  return parts[0] + "?w=400&monochrome=9F9F9F";
};

const SponsorItem: React.SFC<ItemProps> = ({ sponsor, color }) => (
  <Box
    sx={{
      backgroundColor: color,
    }}
  >
    <Link
      target="_blank"
      path={sponsor.link!}
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
            top: "35px",
            bottom: "35px",
            left: "40px",
            right: "40px",
          }}
        >
          <LazyLoad offset={100}>
            <img
              sx={{
                width: "100%",
                height: "100%",
                objectFit: "contain",
              }}
              src={getImageUrl(sponsor.image)}
              alt={sponsor.name}
            />
          </LazyLoad>
        </Box>
      )}
    </Link>
  </Box>
);

export const SponsorsGrid: React.SFC<Props> = ({ sponsors, color }) => {
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
