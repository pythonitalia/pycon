/** @jsxRuntime classic */

/** @jsx jsx */
import { Fragment, useCallback } from "react";
import { FormattedMessage } from "react-intl";
import { Box, Flex, Grid, Heading, jsx, Text } from "theme-ui";

import { GetStaticPaths, GetStaticProps } from "next";
import { useRouter } from "next/router";

import { addApolloState, getApolloClient } from "~/apollo/client";
import { Alert } from "~/components/alert";
import { Article } from "~/components/article";
import { BackToMarquee } from "~/components/back-to-marquee";
import { Button } from "~/components/button/button";
import { BlogPostIllustration } from "~/components/illustrations/blog-post";
import { Link } from "~/components/link";
import { MetaTags } from "~/components/meta-tags";
import { PageLoading } from "~/components/page-loading";
import { useLoginState } from "~/components/profile/hooks";
import { SpeakerDetail } from "~/components/speaker-detail";
import { compile } from "~/helpers/markdown";
import { prefetchSharedQueries } from "~/helpers/prefetch";
import {
  queryAllTalks,
  queryTalk,
  useBookScheduleItemMutation,
  useCancelBookingScheduleItemMutation,
  useTalkQuery,
} from "~/types";

export const TalkPage = () => {
  const router = useRouter();
  const slug = router.query.slug as string;
  const day = router.query.day as string;
  const [isLoggedIn] = useLoginState();

  const { data, loading: isLoadingTalkData } = useTalkQuery({
    returnPartialData: true,
    variables: {
      code: process.env.conferenceCode,
      slug,
      isLoggedIn,
    },
  });
  const [
    executeBookScheduleItem,
    { data: bookSpotData, loading: isBookingSpot },
  ] = useBookScheduleItemMutation();
  const [
    executeCancelBooking,
    { loading: isCancellingBooking },
  ] = useCancelBookingScheduleItemMutation();

  const goBack = useCallback(() => {
    router.push(`/schedule/${day}`);
  }, [day]);

  if (!data) {
    return <PageLoading titleId="global.loading" />;
  }

  const { talk } = data.conference;

  const description = talk.submission
    ? talk.submission.abstract
    : talk.description;
  const elevatorPitch = talk.submission ? talk.submission.elevatorPitch : null;

  const bookScheduleItem = () => {
    executeBookScheduleItem({
      variables: {
        id: talk?.id,
      },
    });
  };

  const cancelBooking = () => {
    executeCancelBooking({
      variables: {
        id: talk?.id,
      },
    });
  };

  return (
    <Fragment>
      <MetaTags title={talk.title} useDefaultSocialCard={false} />

      <Grid
        gap={5}
        sx={{
          mx: "auto",
          px: 3,
          py: 5,
          maxWidth: "container",
          gridTemplateColumns: [null, null, "2fr 1fr"],
        }}
      >
        <Box>
          <Article title={talk.title}>
            {elevatorPitch && <Box>{compile(elevatorPitch).tree}</Box>}

            <Heading as="h2">Abstract</Heading>

            {compile(description).tree}
          </Article>
        </Box>

        <Flex sx={{ mb: 5, flexDirection: ["column-reverse", "column"] }}>
          <Flex
            sx={{
              position: "relative",
              justifyContent: "flex-end",
              alignItems: "flex-start",
            }}
          >
            <BlogPostIllustration
              sx={{
                width: "80%",
              }}
            />

            {talk.speakers.length > 0 && (
              <Box
                sx={{
                  border: "primary",
                  p: 4,
                  backgroundColor: "cinderella",
                  width: "80%",
                  position: "absolute",
                  left: 0,
                  top: talk.image ? "90%" : "70%",
                }}
              >
                <Text sx={{ fontWeight: "bold" }}>
                  <FormattedMessage id="blog.author" />
                </Text>

                <Text>
                  {talk.speakers.map(({ fullName }) => fullName).join(" & ")}
                </Text>
              </Box>
            )}
          </Flex>
          {talk.hasLimitedCapacity && (
            <Flex
              sx={{
                mt: [0, 5],
                mb: [5, 0],
                alignItems: isLoggedIn ? "stretch" : "flex-start",
                flexDirection: "column",
              }}
            >
              <Text sx={{ fontWeight: "bold" }}>
                <FormattedMessage id="talk.bookToAttend" />
              </Text>

              {talk.userHasSpot && (
                <Alert variant="success">
                  <FormattedMessage id="talk.spotReserved" />
                </Alert>
              )}

              {!talk.userHasSpot && !isLoadingTalkData && !talk.hasSpacesLeft && (
                <Alert variant="info">
                  <FormattedMessage id="talk.eventIsFull" />
                </Alert>
              )}

              {isLoggedIn && isLoadingTalkData && (
                <Alert variant="info">
                  <FormattedMessage id="global.loading" />
                </Alert>
              )}

              {isLoggedIn && talk.hasSpacesLeft && !talk.userHasSpot && (
                <Button
                  loading={isBookingSpot}
                  onClick={bookScheduleItem}
                  sx={{ my: 2 }}
                >
                  <FormattedMessage id="talk.bookCta" />
                </Button>
              )}

              {!isLoggedIn && (
                <Link variant="arrow-button" path="/login" sx={{ my: 2 }}>
                  <FormattedMessage id="talk.loginToBook" />
                </Link>
              )}

              {isLoggedIn && talk.userHasSpot && (
                <Button
                  loading={isCancellingBooking}
                  onClick={cancelBooking}
                  sx={{ my: 2 }}
                >
                  <FormattedMessage id="talk.unregisterCta" />
                </Button>
              )}

              {bookSpotData?.bookScheduleItem?.__typename ===
                "UserNeedsConferenceTicket" && (
                <Alert variant="alert">
                  <FormattedMessage
                    id="talk.buyATicket"
                    values={{
                      link: (
                        <Link path="/tickets">
                          <FormattedMessage id="talk.buyATicketCTA" />
                        </Link>
                      ),
                    }}
                  />
                </Alert>
              )}

              {bookSpotData?.bookScheduleItem?.__typename ===
                "ScheduleItemIsFull" && (
                <Alert variant="alert">
                  <FormattedMessage id="talk.eventIsFull" />
                </Alert>
              )}

              <FormattedMessage
                id="talk.spacesLeft"
                values={{
                  spacesLeft: talk.spacesLeft,
                }}
              />
            </Flex>
          )}
        </Flex>
      </Grid>

      <Box sx={{ borderTop: "primary" }} />

      <Grid
        gap={5}
        sx={{
          mx: "auto",
          px: 3,
          py: 5,
          maxWidth: "container",
          gridTemplateColumns: [null, "1fr 2fr"],
        }}
      >
        {talk.speakers.map((speaker) => (
          <SpeakerDetail speaker={speaker} key={speaker.fullName} />
        ))}
      </Grid>

      <BackToMarquee backTo="schedule" goBack={goBack} />
    </Fragment>
  );
};

export const getStaticProps: GetStaticProps = async ({ locale, params }) => {
  const slug = params.slug as string;
  const client = getApolloClient();

  await Promise.all([
    prefetchSharedQueries(client, locale),
    queryTalk(client, {
      code: process.env.conferenceCode,
      slug,
      isLoggedIn: false,
    }),
  ]);

  return addApolloState(client, {
    props: {},
  });
};

export const getStaticPaths: GetStaticPaths = async () => {
  const client = getApolloClient();

  const {
    data: {
      conference: { talks },
    },
  } = await queryAllTalks(client, {
    code: process.env.conferenceCode,
  });

  const paths = [
    ...talks.map((talk) => ({
      params: {
        slug: talk.slug,
      },
      locale: "en",
    })),
    ...talks.map((talk) => ({
      params: {
        slug: talk.slug,
      },
      locale: "it",
    })),
  ];

  return {
    paths,
    fallback: "blocking",
  };
};

export default TalkPage;
