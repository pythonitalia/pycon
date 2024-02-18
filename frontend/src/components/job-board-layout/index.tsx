import {
  Button,
  Grid,
  GridColumn,
  Heading,
  LayoutContent,
  Page,
  Section,
  Spacer,
  Text,
} from "@python-italia/pycon-styleguide";
import React from "react";
import { FormattedMessage } from "react-intl";

import { JobListingAccordion } from "~/components/job-listing-accordion";
import { compile } from "~/helpers/markdown";
import { AllJobListingsQueryResult } from "~/types";

import { Article } from "../article";
import { MetaTags } from "../meta-tags";

type Props = {
  jobListings: AllJobListingsQueryResult["data"]["jobListings"];
  jobListing: AllJobListingsQueryResult["data"]["jobListings"][0];
  onMobileShowOnly: "jobListings" | "jobListing";
};

export const JobBoardLayout = ({
  jobListings,
  jobListing,
  onMobileShowOnly,
}: Props) => {
  return (
    <Page endSeparator={false}>
      <FormattedMessage id="jobboard.title">
        {(text) => <MetaTags title={text} />}
      </FormattedMessage>
      <Section>
        <Heading size="display1">
          <FormattedMessage id="jobboard.title" />
        </Heading>
      </Section>

      <Section>
        <Grid cols={12}>
          <GridColumn colSpan={4}>
            <LayoutContent
              showFrom={
                onMobileShowOnly === "jobListing" ? "desktop" : "mobile"
              }
              as="ul"
              fullScreenHeight
              overflow="scroll"
            >
              {jobListings.map((job) => (
                <JobListingAccordion key={job.id} job={job} />
              ))}
            </LayoutContent>
          </GridColumn>
          <GridColumn colSpan={8}>
            <LayoutContent
              showFrom={
                onMobileShowOnly === "jobListings" ? "desktop" : "mobile"
              }
              fullScreenHeight
              overflow="scroll"
            >
              <Heading size={2}>{jobListing.title}</Heading>
              <Spacer size="small" />
              <Text size={2} color="grey-500">
                {jobListing.company}
              </Text>
              <Spacer size="large" />
              <Article>{compile(jobListing.description).tree}</Article>
              <Spacer size="xl" />
              {jobListing.applyUrl && (
                <Button href={jobListing.applyUrl} variant="secondary">
                  <FormattedMessage id="jobboard.applyNow" />
                </Button>
              )}
            </LayoutContent>
          </GridColumn>
        </Grid>
      </Section>
    </Page>
  );
};
