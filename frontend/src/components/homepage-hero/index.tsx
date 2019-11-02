/** @jsx jsx */

import { Box } from "@theme-ui/components";
import { Link, useStaticQuery, graphql } from "gatsby";
import Img, { GatsbyImageProps } from "gatsby-image";
import React from "react";
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
      }}
    >
      <Box
        sx={{
          paddingBottom: ["100vh", "53%"],
          backgroundImage: `url(${hero!.childImageSharp!.fluid!.src})`,
          backgroundPosition: "center",
          backgroundRepeat: "no-repeat",
          backgroundSize: "cover",
        }}
      />

      <Link
        to="/tickets"
        sx={{
          position: "absolute",
          bottom: [20, 30],
          left: [20, 30],
        }}
      >
        <BuyTicketsCTA
          sx={{
            width: [122, 150],
            height: [120, 150],
          }}
        />
      </Link>
    </Box>
  );
};
