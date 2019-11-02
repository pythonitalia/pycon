/** @jsx jsx */

import { Box, Flex, Grid, Heading, Text } from "@theme-ui/components";
import { graphql, useStaticQuery } from "gatsby";
import Img from "gatsby-image";
import { Fragment } from "react";
import { jsx } from "theme-ui";

type SpeakerProps = {
  last?: boolean;
};

const Speaker = ({ last }: SpeakerProps) => {
  const {
    file: { childImageSharp },
  } = useStaticQuery(graphql`
    {
      file(relativePath: { eq: "images/speaker-example.jpg" }) {
        childImageSharp {
          fixed(width: 500, height: 500, fit: COVER, grayscale: true) {
            ...GatsbyImageSharpFixed
          }
        }
      }
    }
  `);

  return (
    <Box
      sx={{
        position: "relative",
        borderLeft: "primary",
        borderRight: last ? "primary" : null,
      }}
    >
      <Box sx={{ display: "inline-block", pt: "100%" }} />
      <Img
        style={{
          position: "absolute",
          top: 0,
          left: 0,
          width: "100%",
          height: "100%",
        }}
        {...childImageSharp}
      />
      <Box
        sx={{
          position: "absolute",
          top: 0,
          left: 0,
          width: "100%",
          height: "100%",
          background: "#79CDE0",
          mixBlendMode: "multiply",
        }}
      />

      <Flex
        sx={{
          p: 3,
          flexDirection: "column",
          justifyContent: "flex-end",
          color: "white",
          position: "absolute",
          top: 0,
          left: 0,
          width: "100%",
          height: "100%",
        }}
      >
        <Heading variant="caps" as="h3">
          Speaker name
        </Heading>
        <Text>Talk title</Text>
      </Flex>
    </Box>
  );
};

export const KeynotersSection = () => (
  <Box sx={{ borderBottom: "primary", borderTop: "primary" }}>
    <Box sx={{ borderBottom: "primary", py: 4 }}>
      <Heading
        as="h1"
        sx={{
          px: 2,
          maxWidth: "container",
          mx: "auto",
        }}
      >
        Keynote speakers
      </Heading>
    </Box>

    <Grid
      columns={3}
      gap={0}
      sx={{
        maxWidth: "container",
        mx: "auto",
      }}
    >
      <Speaker />
      <Speaker />
      <Speaker last={true} />
    </Grid>
  </Box>
);
