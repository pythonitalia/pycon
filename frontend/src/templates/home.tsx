/** @jsx jsx */
import css from "@styled-system/css";
import { Box, Flex, Grid, Heading, Text } from "@theme-ui/components";
import { Link } from "fannypack";
import { graphql } from "gatsby";
import Img from "gatsby-image";
import { Fragment } from "react";
import { jsx } from "theme-ui";

import { EventCard } from "../components/home-events/event-card";
import { HomepageHero } from "../components/homepage-hero";
import { KeynotersSection } from "../components/keynoters-section";
import { Marquee } from "../components/marquee";
import { HomePageQuery } from "../generated/graphql";

export default ({ data }: { data: HomePageQuery }) => {
  const {
    backend: { conference },
  } = data;

  return (
    <Fragment>
      <HomepageHero />

      <Marquee message={conference.marquee!} />

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

          <Heading as="h2" sx={{ color: "yellow", fontSize: 3, mb: 3 }}>
            {conference.proposalsSubtitle}
          </Heading>

          <Text as="p">{conference.proposalsText}</Text>
        </Box>
      </Grid>

      {conference.events.length > 0 && (
        <Fragment>
          <Box sx={{ borderBottom: "primary", borderTop: "primary" }}>
            <Box sx={{ py: 4 }}>
              <Heading
                as="h1"
                sx={{
                  px: 2,
                  maxWidth: "container",
                  mx: "auto",
                }}
              >
                Conference Highlights
              </Heading>
            </Box>
          </Box>

          <Grid
            columns={4}
            gap={"3px"}
            sx={{ px: "3px", borderBottom: "primary", background: "black" }}
          >
            {conference.events.map((event, index) => (
              <EventCard event={event} key={index} />
            ))}

            {conference.events.length < 4 && (
              <Box
                sx={{
                  gridColumnStart: conference.events.length + 1,
                  gridColumnEnd: 5,
                  background: "white",
                }}
              />
            )}
          </Grid>
        </Fragment>
      )}

      <Box
        sx={{
          borderBottom: "primary",
        }}
      >
        <Grid
          sx={{
            py: 5,
            px: 2,

            gridTemplateColumns: [null, null, "8fr 2fr 10fr"],

            maxWidth: "container",
            mx: "auto",
          }}
        >
          <Flex
            sx={{
              flexDirection: "column",
              justifyContent: "center",
            }}
          >
            <Heading as="h1">Getting there</Heading>
            <Text
              sx={{
                mt: 4,
              }}
              as="p"
            >
              Donec rutrum congue leo eget malesuada. Lorem ipsum dolor sit
              amet. Donec rutrum congue leo eget malesuada. Lorem ipsum dolor
              sit amet, consectetur adipiscing elit. Vivamus magna justo,
              lacinia eget consectetur sed, convallis at tellus.
            </Text>
          </Flex>

          <a
            target="_blank"
            rel="noopener noreferrer"
            href={conference.map!.link!}
            sx={{
              width: "100%",
              height: 420,

              display: "block",

              mt: [3, 3, 0],

              gridColumnStart: [null, null, 3],

              border: "3px solid #000",

              backgroundImage: `url("${conference.map!.image}")`,
              backgroundSize: "cover",
              backgroundRepeat: "no-repeat",
              backgroundPosition: "center",
            }}
          />
        </Grid>
      </Box>

      <Box sx={{ borderBottom: "primary" }}>
        <Box sx={{ py: 4 }}>
          <Heading
            as="h1"
            sx={{
              px: 2,
              maxWidth: "container",
              mx: "auto",
            }}
          >
            Sponsors
          </Heading>
        </Box>
      </Box>

      <Box sx={{ pb: 5 }}>
        {conference.sponsorsByLevel.map(({ level, sponsors }) => (
          <Box key={level}>
            <Heading
              sx={{
                maxWidth: "container",
                mx: "auto",
                my: 3,
              }}
            >
              <Box
                as="span"
                sx={{
                  transform: "rotate(90deg)",
                  transformOrigin: "0 0",
                  top: 5,
                  p: 2,
                  left: -20,
                }}
                css={css`
                  @media (min-width: 1310px) {
                    position: relative;
                    display: inline-block;
                    padding: 0;
                  }
                `}
              >
                {level}
              </Box>
            </Heading>

            <Grid
              columns={3}
              gap={1}
              sx={{
                maxWidth: "container",
                mx: "auto",
                border: "primary",
                background: "black",
              }}
            >
              {sponsors.map(sponsor => (
                <Box
                  sx={{
                    backgroundColor: "yellow",
                  }}
                  key={sponsor.name}
                >
                  <Link
                    href={sponsor.link!}
                    sx={{
                      filter: "saturate(0)",
                      transition: "0.3s filter ease-in-out",
                      position: "relative",
                      display: "block",
                      "&:hover": {
                        filter: "none",
                      },
                    }}
                  >
                    <Box sx={{ display: "inline-block", pt: "40%" }} />

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
              ))}
            </Grid>
          </Box>
        ))}
      </Box>
    </Fragment>
  );
};

export const query = graphql`
  query HomePage($language: String!) {
    backend {
      conference {
        name(language: $language)
        introduction(language: $language)

        marquee: copy(key: "marquee", language: $language)
        introTitle: copy(key: "intro-title-1", language: $language)
        introText: copy(key: "intro-text-1", language: $language)

        proposalsTitle: copy(key: "proposals-title", language: $language)
        proposalsSubtitle: copy(key: "proposals-subtitle", language: $language)
        proposalsText: copy(key: "proposals-text", language: $language)

        eventsIntro: copy(key: "events-intro", language: $language)
        deadlinesIntro: copy(key: "deadlines-intro", language: $language)

        map {
          image(width: 1280, height: 400, zoom: 15)
          link
        }

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
              fixed(grayscale: true, width: 600, height: 600) {
                ...GatsbyImageSharpFixed
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
                  maxWidth: 800
                  maxHeight: 500
                  background: "transparent"
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
