/** @jsxRuntime classic */

/** @jsx jsx */
import React, { Fragment, useCallback, useState } from "react";
import { FormattedMessage } from "react-intl";
import { Box, Grid, Heading, jsx, Text } from "theme-ui";

import { EnglishIcon } from "~/components/icons/english";
import { ItalianIcon } from "~/components/icons/italian";
import { Link } from "~/components/link";
import { compile } from "~/helpers/markdown";
import { useSendVoteMutation } from "~/types";

import { VOTE_VALUES, VoteSelector } from "./vote-selector";

type Submission = {
  id: string;
  title: string;
  abstract?: string | null;
  elevatorPitch?: string | null;
  notes?: string | null;
  myVote?: {
    value: number;
  } | null;
  topic?: {
    id: string;
    name: string;
  } | null;
  tags?:
    | {
        id: string;
        name: string;
      }[]
    | null;
  audienceLevel?: {
    id: string;
    name: string;
  } | null;
  duration?: {
    id: string;
    name: string;
    duration: number;
  } | null;
  languages?:
    | {
        id: string;
        name: string;
        code: string;
      }[]
    | null;
  speaker?: {
    fullName: string;
  } | null;
};

type Props = {
  backgroundColor: string;
  headingColor: string;
  showVoting?: boolean;
  renderTitle?: (title: string) => string | React.ReactElement;
  vote?: {
    id: string;
    value: number;
  } | null;
  onVote?: (submission: Submission) => void;
  submission: Submission;
};

const usePersistedOpenState = (
  submissionId: string,
): [boolean, (value: boolean) => void] => {
  const key = `@submission-accordion@${submissionId}`;
  const [open, setOpen] = useState(() => {
    const value =
      typeof window === "undefined" ? null : window.sessionStorage.getItem(key);

    return value !== null;
  });

  const setValue = (value: boolean) => {
    setOpen(value);

    if (value) {
      window.sessionStorage.setItem(key, "true");
    } else {
      window.sessionStorage.removeItem(key);
    }
  };

  return [open, setValue];
};

export const SubmissionAccordion = ({
  backgroundColor,
  headingColor,
  vote,
  onVote,
  submission,
  renderTitle,
  showVoting = true,
  submission: {
    id,
    title,
    elevatorPitch,
    topic,
    tags,
    audienceLevel,
    duration,
    languages,
    speaker,
  },
}: Props) => {
  const [open, setOpen] = usePersistedOpenState(id);
  const toggleAccordion = useCallback(() => {
    setOpen(!open);
  }, [open]);

  const [
    sendVote,
    { loading, error, data: submissionData },
  ] = useSendVoteMutation({
    update(cache, { data }) {
      if (error || data?.sendVote.__typename === "SendVoteErrors") {
        return;
      }

      cache.modify({
        id: cache.identify({
          id,
          __typename: "Submission",
        }),
        fields: {
          myVote() {
            return data!.sendVote;
          },
        },
      });
    },
  });

  const onSubmitVote = useCallback(
    (value) => {
      if (loading || !onVote) {
        return;
      }

      const prevVote = vote ?? { id: `${Math.random()}` };

      onVote(submission);

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

  const isInItalian = submission.languages?.find((l) => l.code === "it");
  const isInEnglish = submission.languages?.find((l) => l.code === "en");
  const hasVote = !!submission.myVote;
  const showMiddleColumn = (showVoting && hasVote) || speaker?.fullName;

  const middleSpace = showMiddleColumn ? "150px" : 0;
  const headerGrid = [`1fr 0px 30px 130px`, `1fr ${middleSpace} 110px 150px`];

  return (
    <Box
      as="li"
      sx={{
        backgroundColor,
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
        <Grid
          sx={{
            maxWidth: "container",
            mx: "auto",
            px: 3,
            justifyContent: "space-between",
            gridTemplateColumns: headerGrid,
            alignItems: "center",
            cursor: "pointer",

            "svg + svg": {
              marginLeft: [0, 1],
              marginTop: [1, 0],
            },
          }}
          onClick={toggleAccordion}
        >
          <Text
            sx={{
              py: 3,
            }}
          >
            {renderTitle ? renderTitle(title) : title}
            {hasVote && (
              <Text
                sx={{
                  fontWeight: "bold",
                  display: [null, "none"],
                  mt: 2,
                }}
              >
                <FormattedMessage
                  id={
                    VOTE_VALUES.find(
                      (i) => i.value === submission.myVote!.value,
                    )!.textId
                  }
                />
              </Text>
            )}
          </Text>

          {showMiddleColumn ? (
            <Text
              sx={{
                fontWeight: "bold",
                py: 3,
                visibility: ["hidden", "visible"],
              }}
            >
              {showVoting && hasVote && (
                <FormattedMessage
                  id={
                    VOTE_VALUES.find(
                      (i) => i.value === submission.myVote!.value,
                    )!.textId
                  }
                />
              )}
              {speaker?.fullName}
            </Text>
          ) : (
            <Box />
          )}

          <Box
            sx={{
              textAlign: "right",
              py: 3,
            }}
          >
            {isInItalian && (
              <ItalianIcon
                sx={{
                  flexShrink: 0,
                  width: [30, 50],
                }}
              />
            )}
            {isInEnglish && (
              <EnglishIcon
                sx={{
                  flexShrink: 0,
                  width: [30, 50],
                }}
              />
            )}
          </Box>

          <Text
            sx={{
              display: "flex",
              alignItems: "center",
              justifyContent: "flex-end",
              textAlign: "center",
              p: 3,
              height: "100%",
              borderLeft: "primary",
              userSelect: "none",
            }}
          >
            <FormattedMessage
              id={open ? "global.accordion.close" : "global.accordion.readMore"}
            />
          </Text>
        </Grid>
      </Box>

      {open && (
        <Fragment>
          {showVoting && (
            <Box sx={{ borderBottom: "primary", py: 3 }}>
              <VoteSelector
                value={vote?.value ?? 0}
                onVote={onSubmitVote}
                sx={{ maxWidth: "container", mx: "auto", px: 3 }}
              />

              <Text
                sx={{
                  mt: [3, 2],
                  px: 3,

                  fontWeight: "bold",
                  maxWidth: "container",
                  mx: "auto",
                }}
              >
                {loading && <FormattedMessage id="voting.sendingVote" />}
                {error && error}
                {submissionData &&
                  submissionData.sendVote.__typename === "SendVoteErrors" && (
                    <Fragment>
                      {submissionData.sendVote.nonFieldErrors}{" "}
                      {submissionData.sendVote.validationSubmission}{" "}
                      {submissionData.sendVote.validationValue}
                    </Fragment>
                  )}
                {submissionData &&
                  submissionData.sendVote.__typename === "VoteType" && (
                    <FormattedMessage id="voting.voteSent" />
                  )}
              </Text>
            </Box>
          )}

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
                      color: headingColor,
                    }}
                  >
                    <FormattedMessage id="voting.elevatorPitch" />
                  </Heading>
                  {compile(elevatorPitch).tree}
                </Fragment>
              )}

              <Box as="footer" sx={{ mt: 4 }}>
                <Link variant="arrow-button" path={`/submission/${id}`}>
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
                  headingColor={headingColor}
                  label={<FormattedMessage id="voting.topic" />}
                  value={topic.name}
                />
              )}
              {audienceLevel && (
                <SubmissionInfo
                  headingColor={headingColor}
                  label={<FormattedMessage id="voting.audienceLevel" />}
                  value={audienceLevel.name}
                />
              )}
              {duration && (
                <SubmissionInfo
                  headingColor={headingColor}
                  label={<FormattedMessage id="voting.length" />}
                  value={
                    <FormattedMessage id="voting.minutes">
                      {(text) => (
                        <>
                          {duration.name} ({duration.duration} {text})
                        </>
                      )}
                    </FormattedMessage>
                  }
                />
              )}
              {tags && (
                <SubmissionInfo
                  headingColor={headingColor}
                  label={<FormattedMessage id="voting.tags" />}
                  value={tags.map((t) => t.name).join(", ")}
                />
              )}
              {languages && (
                <SubmissionInfo
                  headingColor={headingColor}
                  label={<FormattedMessage id="voting.languages" />}
                  value={languages.map((t) => t.name).join(", ")}
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
  headingColor: string;
};

const SubmissionInfo: React.SFC<SubmissionInfoProps> = ({
  label,
  value,
  headingColor,
}) => (
  <li
    sx={{
      "& + &": {
        mt: 3,
      },
    }}
  >
    <Text
      sx={{
        color: headingColor,
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
