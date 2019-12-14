/** @jsx jsx */
import { useQuery } from "@apollo/react-hooks";
import { RouteComponentProps } from "@reach/router";
import { Box, Button, Flex, Grid, Heading, Text } from "@theme-ui/components";
import { Fragment } from "react";
import { FormattedMessage } from "react-intl";
import { jsx } from "theme-ui";

import {
  SubmissionQuery,
  SubmissionQueryVariables,
} from "../../generated/graphql-backend";
import { compile } from "../../helpers/markdown";
import { Link } from "../link";
import { MetaTags } from "../meta-tags";
import { Tag } from "../tag";
import SUBMISSION_QUERY from "./submission.graphql";

export const SubmissionPage = ({ id }: RouteComponentProps<{ id: string }>) => {
  const { loading, error, data } = useQuery<
    SubmissionQuery,
    SubmissionQueryVariables
  >(SUBMISSION_QUERY, {
    variables: {
      id: id!,
    },
  });

  if (loading || !data) {
    return (
      <FormattedMessage id="submission.loading">
        {text => (
          <Fragment>
            <MetaTags title={text} />

            <Heading>{text}...</Heading>
          </Fragment>
        )}
      </FormattedMessage>
    );
  }

  if (!data.submission) {
    return (
      <FormattedMessage id="submission.notFound">
        {text => (
          <Fragment>
            <MetaTags title={text} />

            <Heading>{text}</Heading>
          </Fragment>
        )}
      </FormattedMessage>
    );
  }

  return (
    <Fragment>
      <MetaTags title={data.submission.title} />

      <Box sx={{ borderTop: "primary" }}>
        <Grid
          sx={{
            mx: "auto",
            px: 3,
            py: 5,
            maxWidth: "container",
            gridColumnGap: 5,
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

              <Text sx={{ mb: 3 }}>{data.submission.topic.name}</Text>

              <Text sx={{ fontWeight: "bold" }}>
                <FormattedMessage id="cfp.audienceLevelLabel" />
              </Text>

              <Text sx={{ mb: 3 }}>{data.submission.audienceLevel.name}</Text>

              <Text sx={{ fontWeight: "bold" }}>
                <FormattedMessage id="cfp.languagesLabel" />
              </Text>

              <Text sx={{ mb: 3 }}>
                {data.submission.languages.map(lang => lang.name).join(", ")}
              </Text>

              <Text sx={{ fontWeight: "bold" }}>
                <FormattedMessage id="cfp.lengthLabel" />
              </Text>

              <Text>
                {data.submission.duration.name} (
                {data.submission.duration.duration}{" "}
                <FormattedMessage id="cfp.minutes" />)
              </Text>
            </Box>

            {data.submission.canEdit && (
              <Link
                variant="buttonFullWidth"
                href={`/:language/submission/${data.submission.id}/edit`}
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
              <Heading sx={{ fontSize: 6 }}>{data.submission.title}</Heading>
            </Flex>

            <Heading sx={{ mb: 2 }}>
              <FormattedMessage id="cfp.abstractLabel" />
            </Heading>

            <Text sx={{ mb: 4 }}>{compile(data.submission.abstract).tree}</Text>

            <Heading sx={{ mb: 2 }}>
              <FormattedMessage id="cfp.elevatorPitchLabel" />
            </Heading>

            <Text sx={{ mb: 4 }}>
              {compile(data.submission.elevatorPitch).tree}
            </Text>

            <Heading sx={{ mb: 2 }}>
              <FormattedMessage id="cfp.notesLabel" />
            </Heading>

            <Text sx={{ mb: 4 }}>{compile(data.submission.notes).tree}</Text>

            <Flex
              sx={{
                flexWrap: "wrap",
                mb: 4,
              }}
            >
              {data.submission.tags.map(tag => (
                <Tag key={tag.id} tag={tag} />
              ))}
            </Flex>
          </Box>
        </Grid>
      </Box>
    </Fragment>
  );
};
