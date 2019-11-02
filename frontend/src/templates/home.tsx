import { Box, Grid, Heading, Text } from "@theme-ui/components";
import { graphql } from "gatsby";
import React from "react";

import { HomepageHero } from "../components/homepage-hero";
import { KeynotersSection } from "../components/keynoters-section";
import { Marquee } from "../components/marquee";
import { HomePageQuery } from "../generated/graphql";

export default ({
  data,
  pageContext,
}: {
  data: HomePageQuery;
  pageContext: { language: string };
}) => {
  const {
    backend: { conference },
  } = data;

  return (
    <>
      <HomepageHero />

      <Marquee message="Hello world" />

      <Grid
        sx={{
          py: 5,
          px: 2,
          maxWidth: "container",
          mx: "auto",
          gridTemplateColumns: [null, "8fr 12fr"],
        }}
      >
        <Heading as="h1" variant="caps">
          {conference.name}
        </Heading>

        <Box>
          <Heading as="h2" sx={{ color: "purple", fontSize: 3, mb: 3 }}>
            {conference.introTitle}
          </Heading>

          <Text as="p">{conference.introText}</Text>
        </Box>
      </Grid>

      <KeynotersSection />

      <Grid
        sx={{
          mt: 4,
          py: 5,
          px: 2,
          maxWidth: "container",
          mx: "auto",
          gridTemplateColumns: [null, "10fr 2fr 9fr"],
        }}
      >
        <Box>
          <Box sx={{ border: "primary" }}>
            <Box sx={{ paddingBottom: "50%", display: "inline-block" }} />
          </Box>
        </Box>

        <Box sx={{ gridColumnStart: [null, 3] }}>
          <Heading as="h1" sx={{ mb: 3 }}>
            {conference.proposalsTitle}
          </Heading>

          <Heading as="h2" sx={{ color: "orange", fontSize: 3, mb: 3 }}>
            {conference.proposalsSubtitle}
          </Heading>

          <Text as="p">{conference.proposalsText}</Text>
        </Box>
      </Grid>
    </>
  );
};

export const query = graphql`
  query HomePage($language: String!) {
    backend {
      conference {
        name(language: $language)
        introduction(language: $language)

        introTitle: copy(key: "intro-title-1", language: $language)
        introText: copy(key: "intro-text-1", language: $language)

        proposalsTitle: copy(key: "proposals-title", language: $language)
        proposalsSubtitle: copy(key: "proposals-subtitle", language: $language)
        proposalsText: copy(key: "proposals-text", language: $language)

        eventsIntro: copy(key: "events-intro", language: $language)
        deadlinesIntro: copy(key: "deadlines-intro", language: $language)

        deadlines {
          name(language: $language)
          description(language: $language)
          start
          end
        }

        faqs {
          question(language: $language)
          answer(language: $language)
        }

        events {
          title
          locationName
          image
          start
          imageFile {
            childImageSharp {
              fluid(
                duotone: { highlight: "#0066FF", shadow: "#0B0040" }
                maxWidth: 600
                maxHeight: 300
                background: "white"
              ) {
                ...GatsbyImageSharpFluid
              }
            }
          }
        }

        sponsorsByLevel {
          level
          sponsors {
            name
            link
            image
            imageFile {
              childImageSharp {
                fluid(
                  fit: CONTAIN
                  maxWidth: 600
                  maxHeight: 300
                  background: "white"
                ) {
                  ...GatsbyImageSharpFluid
                }
              }
            }
          }
        }
      }
    }
  }
`;
