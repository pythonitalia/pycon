/** @jsxRuntime classic */
/** @jsx jsx */
import { Fragment } from "react";
import { FormattedMessage } from "react-intl";
import { Box, Flex, Grid, Heading, jsx, Text } from "theme-ui";

import { GridSlider } from "~/components/grid-slider";
import { EventCard } from "~/components/home-events/event-card";
import { HomepageHero } from "~/components/homepage-hero";
import { KeynotersSection } from "~/components/keynoters-section";
import { Link } from "~/components/link";
import { MapWithLink } from "~/components/map-with-link";
import { Marquee } from "~/components/marquee";
import { MetaTags } from "~/components/meta-tags";
import { SponsorsSection } from "~/components/sponsors-section";
import { YouTubeLite } from "~/components/youtube-lite";
import { formatDeadlineDate, formatDeadlineTime } from "~/helpers/deadlines";
import { useCurrentLanguage } from "~/locale/context";
import { useIndexPageQuery } from "~/types";

export const HomePage = () => {
  const language = useCurrentLanguage();
  const { loading, data } = useIndexPageQuery({
    variables: {
      code: process.env.conferenceCode!,
      language,
    },
  });

  if (loading || !data) {
    return null;
  }

  const { conference, blogPosts } = data;

  return (
    <Fragment>
      <FormattedMessage id="home.title">
        {(text) => <MetaTags title={text} />}
      </FormattedMessage>
      <HomepageHero />

      <Marquee message={conference.marquee!} />

      <Grid
        sx={{
          py: 5,
          px: 3,
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

          <Text as="p" sx={{ mb: 3 }}>
            {conference.introText}
          </Text>
        </Box>
      </Grid>

      <KeynotersSection />

      <Grid
        sx={{
          py: 5,
          px: 3,
          maxWidth: "container",
          mx: "auto",
          gridTemplateColumns: [null, null, "10fr 2fr 9fr"],
          display: "none",
        }}
      >
        <Box sx={{ mb: [4, 4, 0] }}>
          <Box sx={{ border: "primary", position: "relative" }}>
            <Box sx={{ paddingBottom: "55%", display: "inline-block" }} />
            <YouTubeLite
              videoId="ZBgwhPFzi_M"
              sx={{
                position: "absolute",
                top: 0,
                left: 0,
                width: "100%",
                height: "100%",
              }}
            />
          </Box>
        </Box>

        <Box sx={{ gridColumnStart: [null, null, 3] }}>
          <Heading as="h1" sx={{ mb: 3 }}>
            {conference.votingTitle}
          </Heading>

          {conference.votingDeadline && (
            <Box
              sx={{
                border: "primary",
                mb: 3,
                display: ["block", "flex"],
                mx: "auto",
                width: ["80%", null, "100%"],
              }}
            >
              <Box
                sx={{
                  flex: 1,
                  p: 3,
                  textAlign: "center",
                  borderRight: [null, "primary"],
                  borderBottom: ["primary", "none"],
                }}
              >
                <Heading variant="caps" color="violet">
                  <FormattedMessage id="home.deadline.begins" />
                </Heading>
                <Box>
                  {formatDeadlineDate(
                    conference.votingDeadline.start,
                    language,
                  )}
                </Box>
                <Box sx={{ fontSize: 0 }}>
                  {formatDeadlineTime(
                    conference.votingDeadline.start,
                    language,
                  )}
                </Box>
              </Box>
              <Box sx={{ flex: 1, p: 3, textAlign: "center" }}>
                <Heading variant="caps" color="orange">
                  <FormattedMessage id="home.deadline.deadline" />
                </Heading>
                <Box>
                  {formatDeadlineDate(conference.votingDeadline.end, language)}
                </Box>
                <Box sx={{ fontSize: 0 }}>
                  {formatDeadlineTime(conference.votingDeadline.end, language)}
                </Box>
              </Box>
            </Box>
          )}

          <Heading as="h2" sx={{ color: "yellow", fontSize: 3, mb: 3 }}>
            {conference.votingSubtitle}
          </Heading>

          <Text as="p" sx={{ mb: 4 }}>
            {conference.votingText}
          </Text>

          <Link path="/[lang]/voting" variant="arrow-button">
            <FormattedMessage id="home.voting.vote" />
          </Link>
        </Box>
      </Grid>

      {conference.events.length > 0 && (
        <GridSlider
          title={<FormattedMessage id="home.conferenceHighlights" />}
          items={conference.events}
          Component={EventCard}
        />
      )}

      <Box
        sx={{
          borderBottom: "primary",
        }}
      >
        <Grid
          sx={{
            py: 5,
            px: 3,

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
            <Heading as="h1">
              <FormattedMessage id="home.gettingThere" />
            </Heading>
            <Text
              sx={{
                mt: 4,
                mb: 3,
              }}
              as="p"
            >
              {conference.gettingThereText}
            </Text>

            <Box>
              <Link
                target="_blank"
                variant="arrow-button"
                path={conference.map!.link!}
              >
                <FormattedMessage id="home.findRoute" />
              </Link>
            </Box>
          </Flex>

          <MapWithLink
            sx={{
              gridColumnStart: [null, null, 3],
            }}
          />
        </Grid>
      </Box>

      <Box sx={{ borderBottom: "primary" }}>
        <Box sx={{ py: 4 }}>
          <Heading
            as="h1"
            sx={{
              px: 3,
              maxWidth: "container",
              mx: "auto",
            }}
          >
            Sponsors
          </Heading>
        </Box>
      </Box>

      <SponsorsSection
        sx={{ mt: 5, pb: 5, borderBottom: "primary" }}
        sponsorsByLevel={conference.sponsorsByLevel}
      />

      <Grid
        columns={[1, 2]}
        sx={{
          px: 3,
          maxWidth: "container",
          mx: "auto",
          display: "none",
        }}
      >
        <Box sx={{ py: 5, pr: [0, 4], borderRight: [null, "primary"] }} />
        <Box sx={{ py: 5, pl: [0, 4] }}>
          <Heading sx={{ fontSize: 5, mb: 4 }}>
            <FormattedMessage id="home.latestNews" />
          </Heading>

          <Box as="ul" sx={{ pl: 3 }}>
            {blogPosts.map((post) => (
              <Box as="li" key={post.slug}>
                <Link
                  sx={{ display: "block" }}
                  path={`/[lang]/blog/${post.slug}`}
                >
                  <Text>{post.title}</Text>
                </Link>
              </Box>
            ))}
          </Box>
        </Box>
      </Grid>
    </Fragment>
  );
};

export default HomePage;
