/** @jsxRuntime classic */

/** @jsx jsx */
import { useState } from "react";
import { FormattedMessage } from "react-intl";
import { Text, Box, Grid, Flex, jsx } from "theme-ui";

import Image from "next/image";

import { compile } from "~/helpers/markdown";
import { JobListing } from "~/types";

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
          gridTemplateColumns: ["1fr 200px", null, "100px 1fr 1fr 200px"],
        }}
        onClick={() => setExpanded(!expanded)}
      >
        <Box
          sx={{
            position: "relative",
            display: ["none", null, "block"],
          }}
        >
          <Image layout="fill" src={job.companyLogo} />
        </Box>
        <Flex
          sx={{
            py: 4,
            alignItems: "center",
            display: ["flex", null, "none"],
          }}
        >
          {job.company} - {job.title}
        </Flex>
        <Flex
          sx={{
            py: 4,
            alignItems: "center",
            display: ["none", null, "flex"],
          }}
        >
          {job.company}
        </Flex>
        <Flex
          sx={{
            py: 4,
            alignItems: "center",
            display: ["none", null, "flex"],
          }}
        >
          {job.title}
        </Flex>
        <Flex
          sx={{
            py: 4,
            alignItems: "center",

            px: 4,
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
            <Box
              sx={{
                "p + p": {
                  pt: 2,
                },
              }}
            >
              {compile(job.description).tree}
            </Box>
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
              <InfoBox labelId="jobboard.company" value={job.company} />
              <InfoBox labelId="jobboard.role" value={job.title} />
            </Grid>
          </Grid>
        </Box>
      )}
    </Box>
  );
};

const InfoBox = ({ labelId, value }: { labelId: string; value: string }) => (
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
