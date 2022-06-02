/** @jsxRuntime classic */

/** @jsx jsx */
import { GetStaticProps } from "next";
import { Fragment } from "react";
import { FormattedMessage } from "react-intl";
import { Box, Grid, Heading, jsx, Text } from "theme-ui";
import { addApolloState, getApolloClient } from "~/apollo/client";
import { Alert } from "~/components/alert";
import { Link } from "~/components/link";

import { MetaTags } from "~/components/meta-tags";
import { prefetchSharedQueries } from "~/helpers/prefetch";
import { queryStreaming, useStreamingQuery } from "~/types";

const formatDate = (date) => {
  const d = new Date(date);
  let month = "" + (d.getMonth() + 1);
  let day = "" + d.getDate();
  const year = d.getFullYear();

  if (month.length < 2) month = "0" + month;
  if (day.length < 2) day = "0" + day;

  return [year, month, day].join("-");
};

export const StreamingPage = () => {
  const today = formatDate(new Date(Date.now()));

  const { data, loading } = useStreamingQuery({
    returnPartialData: true,
    variables: {
      code: process.env.conferenceCode,
    },
    pollInterval: 1000 * 60 * 3,
  });

  const day = data?.conference.days
    ?.filter((item) => item.day === today)
    .shift();

  return (
    <Fragment>
      <MetaTags title="streamings" useDefaultSocialCard={false} />

      <Box sx={{ borderTop: "primary" }}>
        {loading && (
          <Alert variant="info">
            <FormattedMessage id="global.loading" />
          </Alert>
        )}
        {!day && (
          <Alert variant="info">
            <FormattedMessage
              id="streaming.notFound"
              defaultMessage="There are no streaming for today"
            />
          </Alert>
        )}

        <Grid
          sx={{
            maxWidth: "container",
            mx: "auto",
            px: 3,
            my: 5,
            gridTemplateColumns: ["1fr", "1fr", "1fr 1fr"],
          }}
          gap={4}
        >
          {day?.rooms
            .filter((room) => room.type !== "training")
            .map((room) => {
              const runningEvent = day.runningEvents.filter(
                (event) =>
                  event.rooms.findIndex((item) => item.id === room.id) !== -1,
              )[0];
              return (
                <Box sx={{ mb: 5 }}>
                  <Heading as="h1" sx={{ mb: 1 }}>
                    {room.name}
                  </Heading>
                  <Text sx={{ mb: 3 }}>{runningEvent?.title ?? "\u00A0"}</Text>
                  <Box
                    sx={{
                      position: "relative",
                      paddingBottom: "56.5%",
                      height: 0,
                    }}
                  >
                    <iframe
                      height="320px"
                      width="100%"
                      src={room.streamingUrl}
                      allow-fullscreen
                      scrolling="no"
                      sx={{
                        position: "absolute",
                        top: 0,
                        left: 0,
                        width: "100%",
                        height: "100%",
                        backgroundColor: "black",
                      }}
                    />
                  </Box>

                  {runningEvent && (
                    <Link
                      path={runningEvent?.slidoUrl}
                      variant="button"
                      target="_blank"
                      sx={{
                        backgroundColor: "yellow",
                        py: 1,
                        mr: "-4px",
                        mt: 3,
                        position: "relative",
                        textTransform: "none",
                        "&:hover": {
                          backgroundColor: "orange",
                        },
                      }}
                    >
                      <FormattedMessage id="streaming.qa" />
                    </Link>
                  )}
                </Box>
              );
            })}
        </Grid>
      </Box>
    </Fragment>
  );
};

export const getStaticProps: GetStaticProps = async ({ locale, params }) => {
  const client = getApolloClient();

  await Promise.all([
    prefetchSharedQueries(client, locale),
    queryStreaming(client, {
      code: process.env.conferenceCode,
    }),
  ]);
  return addApolloState(client, {
    props: {},
  });
};

export default StreamingPage;
