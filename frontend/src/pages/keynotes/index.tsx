/** @jsxRuntime classic */

/** @jsx jsx */
import { Fragment } from "react";
import { Box, Grid, Flex, Heading, jsx } from "theme-ui";

import { GetStaticProps } from "next";

import { addApolloState, getApolloClient } from "~/apollo/client";
import { Article } from "~/components/article";
import { KeynotesIllustration } from "~/components/illustrations/keynotes";
import { KeynoteSlide } from "~/components/keynoters-section/keynote-slide";
import { MetaTags } from "~/components/meta-tags";
import { prefetchSharedQueries } from "~/helpers/prefetch";
import { useCurrentLanguage } from "~/locale/context";
import { Keynote, queryKeynotesPage, useKeynotesPageQuery } from "~/types";

const KeynotesPage = () => {
  const language = useCurrentLanguage();
  const {
    data: {
      conference: { title, subtitle, description, keynotes },
    },
  } = useKeynotesPageQuery({
    variables: {
      conference: process.env.conferenceCode,
      language,
    },
  });
  return (
    <Fragment>
      <MetaTags title="Keynotes" />
      <Box
        sx={{
          borderTop: "primary",
        }}
      />

      <Grid
        gap={[0, null, 5]}
        sx={{
          mx: "auto",
          px: 3,
          py: 5,
          maxWidth: "container",
          gridTemplateColumns: [null, null, "1fr 1fr"],
        }}
      >
        <Box>
          <Article title={title}>
            {subtitle && (
              <Heading as="h3" color="violet">
                {subtitle}
              </Heading>
            )}

            <Box>{description}</Box>
          </Article>
        </Box>
        <Box>
          <Flex
            sx={{
              position: "relative",
              justifyContent: ["flex-start", null, "flex-end"],
              alignItems: "flex-start",
            }}
          >
            <KeynotesIllustration
              sx={{
                width: ["100%", null, "80%"],
              }}
            />
          </Flex>
        </Box>
      </Grid>

      <Box
        sx={{
          borderTop: "primary",
          pb: 5,
        }}
      />

      <Grid
        gap={[3, 3, 5]}
        sx={{
          gridTemplateColumns: ["1fr", "1fr 1fr", "1fr 1fr 1fr"],
          mx: "auto",
          px: 3,
          pb: 5,
          maxWidth: "container",
        }}
      >
        {keynotes.map((keynote: Keynote) => (
          <KeynoteSlide standalone={true} {...keynote} />
        ))}
      </Grid>
    </Fragment>
  );
};

export const getStaticProps: GetStaticProps = async ({ locale }) => {
  const client = getApolloClient();

  await Promise.all([
    prefetchSharedQueries(client, locale),
    queryKeynotesPage(client, {
      conference: process.env.conferenceCode,
      language: locale,
    }),
  ]);

  return addApolloState(client, {
    props: {},
  });
};

export default KeynotesPage;
