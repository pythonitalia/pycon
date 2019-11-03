/** @jsx jsx */

import { Box } from "@theme-ui/components";
import { graphql, Link, useStaticQuery } from "gatsby";
import { jsx } from "theme-ui";

import { HomepageHeroQuery } from "../../generated/graphql";
import { BuyTicketsCTA } from "./buy-tickets-cta";

type Props = {};

export const HomepageHero: React.SFC<Props> = props => {
  const { hero } = useStaticQuery<HomepageHeroQuery>(graphql`
    query HomepageHero {
      hero: file(name: { eq: "homepage-hero" }) {
        childImageSharp {
          fluid(maxWidth: 1920) {
            ...GatsbyImageSharpFluid
          }
        }
      }
    }
  `);

  return (
    <Box
      sx={{
        position: "relative",
        mt: [-100, -180],
      }}
    >
      <Box
        sx={{
          paddingBottom: ["70vh", "53%"],
          backgroundImage: `url(${hero!.childImageSharp!.fluid!.src})`,
          backgroundPosition: "center",
          backgroundRepeat: "no-repeat",
          backgroundSize: "cover",
        }}
      />

      <Box
        sx={{
          position: "absolute",
          bottom: [20, 30],
          left: [0],

          width: "100%",
        }}
      >
        <Box
          sx={{
            maxWidth: "largeContainer",
            width: "100%",
            mx: "auto",
          }}
        >
          <Link
            to="/tickets"
            sx={{
              px: 2,
            }}
          >
            <BuyTicketsCTA
              sx={{
                width: ["20vw", "10vw"],
                height: ["20vw", "10vw"],
              }}
            />
          </Link>
        </Box>
      </Box>
    </Box>
  );
};
