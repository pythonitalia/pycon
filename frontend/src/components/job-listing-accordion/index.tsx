/** @jsxRuntime classic */

/** @jsx jsx */
import React, { useState } from "react";
import { FormattedMessage } from "react-intl";
import QRCode from "react-qr-code";
import { Text, Box, Grid, Flex, jsx } from "theme-ui";

import { compile } from "~/helpers/markdown";
import { JobListing } from "~/types";

import { Article } from "../article";
import { Link } from "../link";

export const JobListingAccordion = ({
  job,
  backgroundColor,
}: {
  job: JobListing;
  backgroundColor: string;
}) => {
  const [expanded, setExpanded] = useState(false);
  return (
    <Box
      as="li"
      sx={{
        borderTop: "primary",
        bg: backgroundColor,
        "&:last-child": {
          borderBottom: "primary",
        },
      }}
    >
      <Grid
        gap={[3, 5]}
        sx={{
          mx: "auto",
          px: 3,
          maxWidth: "container",
          cursor: "pointer",
          gridTemplateColumns: ["1fr 100px", null, "100px 1fr 1fr 250px 200px"],
        }}
        onClick={() => setExpanded(!expanded)}
      >
        <Box
          sx={{
            position: "relative",
            display: ["none", null, "block"],
            borderRight: job.companyLogo ? "primary" : null,
            borderLeft: job.companyLogo ? "primary" : null,
          }}
        >
          {job.companyLogo && (
            <img
              loading="lazy"
              sx={{
                width: "100%",
                height: "100%",
                objectFit: "contain",
                padding: "10px !important",
              }}
              src={job.companyLogo}
            />
          )}
        </Box>
        <AccordionColumn
          sx={{
            display: ["flex", null, "none"],
          }}
        >
          {job.company} - {job.title}
        </AccordionColumn>
        <AccordionColumn>{job.company}</AccordionColumn>
        <AccordionColumn>{job.title}</AccordionColumn>
        <AccordionColumn sx={{ p: 2 }}>
          {job.applyUrl && <QRCode size={100} value={job.applyUrl} />}
        </AccordionColumn>
        <Flex
          sx={{
            py: [2, 4],
            px: [2, 4],
            alignItems: "center",
            borderLeft: "primary",
          }}
        >
          <FormattedMessage
            id={
              expanded ? "global.accordion.close" : "global.accordion.readMore"
            }
          />
        </Flex>
      </Grid>
      {expanded && (
        <Box
          sx={{
            borderTop: "primary",
          }}
        >
          <Grid
            gap={[4, 2]}
            sx={{
              mx: "auto",
              px: 3,
              py: [4, 5],
              maxWidth: "container",
              gridTemplateColumns: ["1fr", "2fr 1fr"],
            }}
          >
            <Article
              sx={{
                mt: 0,
                mb: 0,
                pr: [0, 2],
                "p + p": {
                  pt: 2,
                },
              }}
            >
              {compile(job.description).tree}
            </Article>
            <Grid
              gap={3}
              sx={{
                justifyItems: "flex-start",
                alignContent: "flex-start",
              }}
            >
              {job.applyUrl && (
                <Link
                  target="_blank"
                  external
                  path={job.applyUrl}
                  variant="arrow-button"
                >
                  <FormattedMessage id="jobboard.applyNow" />
                </Link>
              )}
              <JobExtraInfo labelId="jobboard.company" value={job.company} />
              <JobExtraInfo labelId="jobboard.role" value={job.title} />
            </Grid>
          </Grid>
        </Box>
      )}
    </Box>
  );
};

const AccordionColumn = ({
  children,
  className,
}: {
  children?: React.ReactNode;
  className?: string;
  sx?: any;
}) => (
  <Flex
    sx={{
      py: 4,
      alignItems: "center",
      display: ["none", null, "flex"],
    }}
    className={className}
  >
    {children}
  </Flex>
);

const JobExtraInfo = ({
  labelId,
  value,
}: {
  labelId: string;
  value: string;
}) => (
  <Box>
    <Text
      sx={{
        textTransform: "uppercase",
        fontWeight: "bold",
        color: "black",
        userSelect: "none",
      }}
    >
      <FormattedMessage id={labelId} />
    </Text>
    <Text>{value}</Text>
  </Box>
);
