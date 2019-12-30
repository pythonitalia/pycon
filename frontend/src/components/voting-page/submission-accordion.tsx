/** @jsx jsx */
import { useMutation } from "@apollo/react-hooks";
import { Box, Button, Grid, Heading, Text } from "@theme-ui/components";
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
    abstract,
    elevatorPitch,
    notes,
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

      const submissions = cachedQuery!.conference.submissions;

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
          borderBottom: open ? "primary" : "",
        }}
      >
        <Grid
          sx={{
            maxWidth: "container",
            mx: "auto",
            py: [3, 0],
            px: [0, 3],
            gridTemplateColumns: [
              null,
              "4fr 6fr 2fr",
              "4fr 6fr 2fr",
              "8fr 6fr 2fr",
            ],
            alignItems: "center",
          }}
        >
          <Text
            sx={{
              px: [2, 0],
            }}
          >
            {title}
          </Text>

          <VoteSelector
            sx={{
              borderLeft: ["none", "primary"],
              borderRight: ["none", "primary"],
              px: [2, 2, 4],
              py: [0, 4],
            }}
            value={vote?.value ?? 0}
            onVote={onVote}
            label={
              loading ? (
                <FormattedMessage id="voting.saving" />
              ) : (
                <FormattedMessage id="voting.vote" />
              )
            }
          />

          <Text
            sx={{
              textTransform: "uppercase",
              userSelect: "none",
              cursor: "pointer",
              px: [2, 0],
            }}
            role="button"
            onClick={toggleAccordion}
          >
            <FormattedMessage id={open ? "voting.close" : "voting.readMore"} />
          </Text>
        </Grid>
      </Box>
      {open && (
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
            {abstract && (
              <Fragment>
                <Heading mb={2} as="h2">
                  <FormattedMessage id="voting.abstract" />
                </Heading>
                {compile(abstract).tree}
              </Fragment>
            )}

            {elevatorPitch && (
              <Fragment>
                <Heading mt={4} mb={2} as="h2">
                  <FormattedMessage id="voting.elevatorPitch" />
                </Heading>
                {compile(elevatorPitch).tree}
              </Fragment>
            )}

            {notes && (
              <Fragment>
                <Heading mt={4} mb={2} as="h2">
                  <FormattedMessage id="voting.notes" />
                </Heading>
                {compile(notes).tree}
              </Fragment>
            )}
          </Box>
          <Box
            as="ul"
            sx={{
              listStyle: "none",
            }}
          >
            <Link
              sx={{
                display: "block",
                mb: 3,
                fontWeight: "bold",
                color: "white",
              }}
              href={`/:language/submission/${id}`}
            >
              <FormattedMessage id="voting.openSubmission" />
            </Link>
            {topic && (
              <SubmisionInfo
                label={<FormattedMessage id="voting.topic" />}
                value={topic.name}
              />
            )}
            {audienceLevel && (
              <SubmisionInfo
                label={<FormattedMessage id="voting.audienceLevel" />}
                value={audienceLevel.name}
              />
            )}
            {duration && (
              <SubmisionInfo
                label={<FormattedMessage id="voting.length" />}
                value={
                  <FormattedMessage id="voting.minutes">
                    {text => `${duration.name} (${duration.duration} ${text})`}
                  </FormattedMessage>
                }
              />
            )}
            {tags && (
              <SubmisionInfo
                label={<FormattedMessage id="voting.tags" />}
                value={tags.map(t => t.name).join(", ")}
              />
            )}
            {languages && (
              <SubmisionInfo
                label={<FormattedMessage id="voting.languages" />}
                value={languages.map(t => t.name).join(", ")}
              />
            )}
          </Box>
        </Grid>
      )}
    </Box>
  );
};

type SubmisionInfoProps = {
  label: string | React.ReactElement;
  value: string | React.ReactElement;
};

const SubmisionInfo: React.SFC<SubmisionInfoProps> = ({ label, value }) => (
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
        fontSize: 3,
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
