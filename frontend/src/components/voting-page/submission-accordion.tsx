/** @jsx jsx */
import { useMutation } from "@apollo/react-hooks";
import { Box, Flex, Grid, Heading, Text } from "@theme-ui/components";
import { Fragment, useCallback, useState } from "react";
import { FormattedMessage } from "react-intl";
import { jsx } from "theme-ui";

import { useConference } from "../../context/conference";
import {
  SendVoteMutation,
  SendVoteMutationVariables,
  VotingSubmissionsQuery,
  VotingSubmissionsQueryVariables,
} from "../../generated/graphql-backend";
import { compile } from "../../helpers/markdown";
import { Link } from "../link";
import SAVE_VOTE from "./save-vote.graphql";
import { VoteSelector } from "./vote-selector";
import VOTING_SUBMISSIONS from "./voting-submissions.graphql";

type Props = {
  vote: {
    id: string;
    value: number;
  } | null;
  submission: {
    id: string;
    title: string;
    abstract?: string | null;
    elevatorPitch?: string | null;
    notes?: string | null;
    topic: {
      id: string;
      name: string;
    } | null;
    tags:
      | {
          id: string;
          name: string;
        }[]
      | null;
    audienceLevel: {
      id: string;
      name: string;
    } | null;
    duration: {
      id: string;
      name: string;
      duration: number;
    } | null;
    languages:
      | {
          id: string;
          name: string;
        }[]
      | null;
  };
};

export const SubmissionAccordion: React.SFC<Props> = ({
  vote,
  submission: {
    id,
    title,
    elevatorPitch,
    topic,
    tags,
    audienceLevel,
    duration,
    languages,
  },
}) => {
  const [open, setOpen] = useState(false);
  const toggleAccordion = useCallback(() => {
    setOpen(o => !o);
  }, []);
  const { code: conferenceCode } = useConference();

  const [sendVote, { loading, error }] = useMutation<
    SendVoteMutation,
    SendVoteMutationVariables
  >(SAVE_VOTE, {
    update(cache, { data }) {
      if (error || data?.sendVote.__typename === "SendVoteErrors") {
        return;
      }

      const cachedQuery = cache.readQuery<
        VotingSubmissionsQuery,
        VotingSubmissionsQueryVariables
      >({
        query: VOTING_SUBMISSIONS,
        variables: {
          conference: conferenceCode,
        },
      });

      const submissions = cachedQuery!.conference.submissions!;

      const updatedSubmissionIndex = submissions.findIndex(i => i.id === id)!;
      const updatedSubmission = {
        ...submissions[updatedSubmissionIndex]!,
      };
      updatedSubmission.myVote = data!.sendVote;
      submissions[updatedSubmissionIndex] = updatedSubmission;

      cache.writeQuery<VotingSubmissionsQuery, VotingSubmissionsQueryVariables>(
        {
          query: VOTING_SUBMISSIONS,
          data: {
            // @ts-ignore
            conference: {
              ...cachedQuery?.conference,
              submissions,
            },
          },
        },
      );
    },
  });

  const onVote = useCallback(
    value => {
      if (loading) {
        return;
      }

      const prevVote = vote ?? { id: `${Math.random()}` };

      sendVote({
        variables: {
          input: {
            submission: id,
            value,
          },
        },
        optimisticResponse: {
          __typename: "Mutation",
          sendVote: {
            __typename: "VoteType",
            ...prevVote,
            value,
          },
        },
      });
    },
    [loading],
  );

  return (
    <Box
      as="li"
      sx={{
        background: "#79CDE0",
        overflow: "hidden",

        "&:last-child": {
          "> div:first-of-type": {
            borderBottom: "primary",
          },
        },
      }}
    >
      <Box
        sx={{
          borderTop: "primary",
          borderBottom: open && "primary",
        }}
      >
        <Flex
          sx={{
            maxWidth: "container",
            mx: "auto",
            justifyContent: "space-between",
            p: 3,
          }}
          onClick={toggleAccordion}
        >
          <Text>{title}</Text>

          <Text>
            <FormattedMessage id={open ? "voting.close" : "voting.readMore"} />
          </Text>
        </Flex>
      </Box>

      {open && (
        <Fragment>
          <Box sx={{ borderBottom: "primary" }}>
            <VoteSelector
              value={vote?.value ?? 0}
              onVote={onVote}
              sx={{ p: 3, maxWidth: "container", mx: "auto" }}
            />
          </Box>
          <Grid
            sx={{
              maxWidth: "container",
              mx: "auto",
              px: 3,
              py: [3, 5],
              gridTemplateColumns: [null, "3fr 1fr"],
              columnGap: 4,
            }}
          >
            <Box>
              {elevatorPitch && (
                <Fragment>
                  <Heading
                    mb={2}
                    as="h2"
                    sx={{
                      fontSize: 2,
                      textTransform: "uppercase",
                      color: "white",
                    }}
                  >
                    <FormattedMessage id="voting.elevatorPitch" />
                  </Heading>
                  {compile(elevatorPitch).tree}
                </Fragment>
              )}

              <Box as="footer" sx={{ mt: 4 }}>
                <Link
                  variant="button"
                  href={`/:language/submission/${id}`}
                  target="_blank"
                >
                  <FormattedMessage id="voting.fullDetails" />
                </Link>
              </Box>
            </Box>
            <Box
              as="ul"
              sx={{
                listStyle: "none",
              }}
            >
              {topic && (
                <SubmissionInfo
                  label={<FormattedMessage id="voting.topic" />}
                  value={topic.name}
                />
              )}
              {audienceLevel && (
                <SubmissionInfo
                  label={<FormattedMessage id="voting.audienceLevel" />}
                  value={audienceLevel.name}
                />
              )}
              {duration && (
                <SubmissionInfo
                  label={<FormattedMessage id="voting.length" />}
                  value={
                    <FormattedMessage id="voting.minutes">
                      {text =>
                        `${duration.name} (${duration.duration} ${text})`
                      }
                    </FormattedMessage>
                  }
                />
              )}
              {tags && (
                <SubmissionInfo
                  label={<FormattedMessage id="voting.tags" />}
                  value={tags.map(t => t.name).join(", ")}
                />
              )}
              {languages && (
                <SubmissionInfo
                  label={<FormattedMessage id="voting.languages" />}
                  value={languages.map(t => t.name).join(", ")}
                />
              )}
            </Box>
          </Grid>
        </Fragment>
      )}
    </Box>
  );
};

type SubmissionInfoProps = {
  label: string | React.ReactElement;
  value: string | React.ReactElement;
};

const SubmissionInfo: React.SFC<SubmissionInfoProps> = ({ label, value }) => (
  <li
    sx={{
      "& + &": {
        mt: 3,
      },
    }}
  >
    <Text
      sx={{
        color: "white",
        fontSize: 2,
        variant: "heading",
        fontWeight: "bold",
        textTransform: "uppercase",
        mb: 2,
      }}
    >
      {label}
    </Text>
    <Text>{value}</Text>
  </li>
);
