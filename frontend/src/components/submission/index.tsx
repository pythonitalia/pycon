/** @jsx jsx */

import React, { Fragment } from "react";
import { FormattedMessage } from "react-intl";
import { Box, Flex, Grid, Heading, jsx, Text } from "theme-ui";

import { Link } from "~/components/link";
import { MetaTags } from "~/components/meta-tags";
import { SubmissionComments } from "~/components/submission-comments/comments";
import { Tag } from "~/components/tag";
import { compile } from "~/helpers/markdown";
import { SubmissionQuery } from "~/types";

type Props = {
  submission: SubmissionQuery["submission"];
};

export const Submission: React.SFC<Props> = ({ submission }) => (
  <Fragment>
    <MetaTags title={submission.title} />

    <Box
      sx={{
        mx: "auto",
        maxWidth: "container",
      }}
    >
      <Grid
        gap={5}
        sx={{
          gridTemplateColumns: [null, null, "2fr 1fr"],
        }}
      >
        <Box sx={{ order: [0, null, 1] }}>
          <Box
            sx={{
              border: "primary",
              p: 4,
              backgroundColor: "cinderella",
              mb: 4,
            }}
          >
            <Text sx={{ fontWeight: "bold" }}>
              <FormattedMessage id="cfp.topicLabel" />
            </Text>

            <Text sx={{ mb: 3 }}>{submission.topic!.name}</Text>

            <Text sx={{ fontWeight: "bold" }}>
              <FormattedMessage id="cfp.audienceLevelLabel" />
            </Text>

            <Text sx={{ mb: 3 }}>{submission.audienceLevel!.name}</Text>

            <Text sx={{ fontWeight: "bold" }}>
              <FormattedMessage id="cfp.languagesLabel" />
            </Text>

            <Text sx={{ mb: 3 }}>
              {submission.languages!.map((lang) => lang.name).join(", ")}
            </Text>

            <Text sx={{ fontWeight: "bold" }}>
              <FormattedMessage id="cfp.lengthLabel" />
            </Text>

            <Text>
              {submission.duration!.name} ({submission.duration!.duration}{" "}
              <FormattedMessage id="cfp.minutes" />)
            </Text>
          </Box>

          {submission.canEdit && (
            <Link
              variant="buttonFullWidth"
              path="/[lang]/submission/[id]/edit"
              params={{
                id: submission.id,
              }}
            >
              Edit
            </Link>
          )}
        </Box>

        <Box>
          <Flex
            sx={{
              alignItems: "center",
              justifyContent: "space-between",
              mb: 4,
            }}
          >
            <Heading sx={{ fontSize: 6 }}>{submission.title}</Heading>
          </Flex>

          <Heading sx={{ mb: 2 }}>
            <FormattedMessage id="cfp.elevatorPitchLabel" />
          </Heading>

          <Box className="article" sx={{ mb: 4 }}>
            {compile(submission.elevatorPitch).tree}
          </Box>

          <Heading sx={{ mb: 2 }}>
            <FormattedMessage id="cfp.abstractLabel" />
          </Heading>

          <Box className="article" sx={{ mb: 4 }}>
            {compile(submission.abstract).tree}
          </Box>

          {submission.notes && (
            <Fragment>
              <Heading sx={{ mb: 2 }}>
                <FormattedMessage id="cfp.notesLabel" />
              </Heading>

              <Box className="article">{compile(submission.notes).tree}</Box>
            </Fragment>
          )}

          <Flex
            sx={{
              flexWrap: "wrap",
              mb: 4,
            }}
          >
            {submission.tags!.map((tag) => (
              <Tag key={tag.id} tag={tag} />
            ))}
          </Flex>
        </Box>
      </Grid>
      <SubmissionComments
        submissionId={submission.id}
        comments={submission.comments}
      />
    </Box>
  </Fragment>
);
