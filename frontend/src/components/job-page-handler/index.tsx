import React from "react";

import { useCurrentLanguage } from "~/locale/context";
import { useAllJobListingsQuery } from "~/types";

import { JobBoardLayout } from "../job-board-layout";

export const JobPageHandler = () => {
  const {
    data: { jobListings },
  } = useAllJobListingsQuery({
    variables: {
      conference: process.env.conferenceCode,
    },
  });

  return (
    <JobBoardLayout
      onMobileShowOnly="jobListings"
      jobListings={jobListings}
      jobListing={jobListings[0]}
    />
  );
};
