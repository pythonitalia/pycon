import {
  Button,
  Grid,
  GridColumn,
  Heading,
  LayoutContent,
  Page,
  Section,
  Spacer,
  StyledHTMLText,
  Text,
} from "@python-italia/pycon-styleguide";
import React from "react";
import { FormattedMessage } from "react-intl";

import { JobListingAccordion } from "~/components/job-listing-accordion";
import type { AllJobListingsQueryResult } from "~/types";

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
              position="sticky"
              style={{
                top: 0,
              }}
              overflow="scroll"
              fullScreenHeight
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
            >
              <Heading size={2}>{jobListing.title}</Heading>
              <Spacer size="small" />
              <Text size={2} color="grey-500">
                {jobListing.company}
              </Text>
              <Spacer size="large" />
              <Article>
                <StyledHTMLText
                  baseTextSize={2}
                  text={jobListing.description}
                />
              </Article>
              <Spacer size="xl" />
              {jobListing.applyUrl && (
                <Button
                  target="_blank"
                  href={jobListing.applyUrl}
                  variant="secondary"
                >
                  <FormattedMessage id="jobboard.applyNow" />
                </Button>
              )}
            </LayoutContent>
            <Spacer size="medium" />
          </GridColumn>
        </Grid>
      </Section>
    </Page>
  );
};
