/** @jsxRuntime classic */

/** @jsx jsx */
import { Fragment } from "react";
import { FormattedMessage } from "react-intl";
import { Box, Grid, Flex, Heading, jsx } from "theme-ui";

import { GetStaticProps } from "next";

import { getApolloClient, addApolloState } from "~/apollo/client";
import { JobListingAccordion } from "~/components/job-listing-accordion";
import { MetaTags } from "~/components/meta-tags";
import { prefetchSharedQueries } from "~/helpers/prefetch";
import { useCurrentLanguage } from "~/locale/context";
import { queryAllJobListings, useAllJobListingsQuery } from "~/types";

const COLORS = ["blue", "orange", "violet", "keppel"];

const JobsBoardPage = () => {
  const language = useCurrentLanguage();
  const {
    data: { jobListings },
  } = useAllJobListingsQuery({
    variables: {
      language,
    },
  });
  console.log("jobListings", jobListings);
  return (
    <Fragment>
      <FormattedMessage id="jobboard.title">
        {(text) => <MetaTags title={text} />}
      </FormattedMessage>
      <Box
        sx={{
          borderTop: "primary",
        }}
      />

      <Box
        sx={{
          mx: "auto",
          px: 3,
          py: 5,
          maxWidth: "container",
        }}
      >
        <Heading as="h1">
          <FormattedMessage id="jobboard.title" />
        </Heading>
      </Box>

      <Box as="ul">
        {jobListings.map((job, index) => (
          <JobListingAccordion
            backgroundColor={COLORS[index % COLORS.length]}
            job={job}
          />
        ))}
      </Box>
    </Fragment>
  );
};

export const getStaticProps: GetStaticProps = async ({ locale }) => {
  const client = getApolloClient();

  await Promise.all([
    prefetchSharedQueries(client, locale),
    queryAllJobListings(client, {
      language: locale,
    }),
  ]);

  return addApolloState(client, {
    props: {},
  });
};

export default JobsBoardPage;
