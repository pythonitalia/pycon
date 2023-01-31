import React from "react";

import { useRouter } from "next/router";

import { useCurrentLanguage } from "~/locale/context";
import { useAllJobListingsQuery } from "~/types";

import { JobBoardLayout } from "../job-board-layout";

export const JobDetailPageHandler = () => {
  const {
    query: { id },
  } = useRouter();
  const language = useCurrentLanguage();
  const {
    data: { jobListings },
  } = useAllJobListingsQuery({
    variables: {
      language,
      conference: process.env.conferenceCode,
    },
  });
  const jobListing = jobListings.find((job) => job.id === id) ?? jobListings[0];

  return (
    <JobBoardLayout
      onMobileShowOnly="jobListing"
      jobListings={jobListings}
      jobListing={jobListing}
    />
  );
};
