import {
  MultiplePartsCard,
  CardPart,
  Grid,
  Heading,
  Spacer,
  Text,
  GridColumn,
  InputNumber,
} from "@python-italia/pycon-styleguide";
import React, { useCallback } from "react";
import { FormattedMessage } from "react-intl";

import { SubmissionAccordionFragment, useSendVoteMutation } from "~/types";

type Props = {
  submission: SubmissionAccordionFragment;
  onVote?: (submission: SubmissionAccordionFragment) => void;
};

export const VotingCard = ({
  onVote,
  submission,
  submission: {
    id,
    title,
    elevatorPitch,
    tags,
    audienceLevel,
    duration,
    languages,
  },
}: Props) => {
  const [sendVote, { loading, error, data: submissionData }] =
    useSendVoteMutation({
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
      if (loading) {
        return;
      }

      const prevVote = submission.myVote ?? { id: `${Math.random()}` };

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

  return (
    <MultiplePartsCard
      openByDefault={false}
      clickablePart="heading"
      expandTarget="content"
    >
      <CardPart
        contentAlign="left"
        id="heading"
        icon="star"
        noBg
        openLabel={<FormattedMessage id="global.accordion.readMore" />}
      >
        <Heading size={3}>{title}</Heading>
      </CardPart>
      <CardPart id="content" contentAlign="left" noBg>
        <InputNumber
          values={[
            {
              value: 1,
              label: <FormattedMessage id="voteSelector.notInterested" />,
            },
            {
              value: 2,
              label: <FormattedMessage id="voteSelector.maybe" />,
            },
            {
              value: 3,
              label: <FormattedMessage id="voteSelector.wantToSee" />,
            },
            {
              value: 4,
              label: <FormattedMessage id="voteSelector.mustSee" />,
            },
          ]}
          value={submission?.myVote.value}
          onClick={onSubmitVote}
        />

        <Text>
          {loading && <FormattedMessage id="voting.sendingVote" />}
          {error && error}
          {submissionData &&
            submissionData.sendVote.__typename === "SendVoteErrors" && (
              <>
                {submissionData.sendVote.nonFieldErrors}{" "}
                {submissionData.sendVote.validationSubmission}{" "}
                {submissionData.sendVote.validationValue}
              </>
            )}
          {submissionData &&
            submissionData.sendVote.__typename === "VoteType" && (
              <FormattedMessage id="voting.voteSent" />
            )}
        </Text>
      </CardPart>
      <CardPart id="content" contentAlign="left" noBg size="none">
        <Grid cols={12} gap="none" divide={true}>
          <GridColumn colSpan={8}>
            <CardPart contentAlign="left" noBg>
              <Text weight="strong" uppercase as="p" size={3}>
                <FormattedMessage id="voting.elevatorPitch" />
              </Text>

              <Spacer size="small" />

              <Text as="p" size={3}>
                {elevatorPitch}
              </Text>
            </CardPart>
          </GridColumn>
          <GridColumn colSpan={3}>
            <CardPart contentAlign="left" noBg>
              <Text weight="strong" uppercase as="p" size={3}>
                <FormattedMessage id="voting.tags" />
              </Text>
              <Spacer size="small" />

              <Text weight="strong" as="p" size={3}>
                {tags.map((tag) => tag.name).join(", ")}
              </Text>
            </CardPart>
          </GridColumn>
        </Grid>
      </CardPart>

      <CardPart id="content" contentAlign="left" noBg size="none">
        <Grid cols={3} gap="none" divide={true}>
          <CardPart contentAlign="left" noBg>
            <Text weight="strong" uppercase as="p" size={3}>
              <FormattedMessage id="voting.length" />
            </Text>

            <Spacer size="small" />

            <Text as="p" weight="strong" size={3}>
              <FormattedMessage id="voting.minutes">
                {(text) => (
                  <>
                    {duration.duration} {text}
                  </>
                )}
              </FormattedMessage>
            </Text>
          </CardPart>
          <CardPart contentAlign="left" noBg>
            <Text weight="strong" uppercase as="p" size={3}>
              <FormattedMessage id="voting.audienceLevel" />
            </Text>
            <Spacer size="small" />

            <Text weight="strong" as="p" size={3}>
              {audienceLevel.name}
            </Text>
          </CardPart>

          <CardPart
            contentAlign="left"
            noBg
            rightSideIcon="arrow"
            rightSideIconBackground="none"
          >
            <Text weight="strong" uppercase as="p" size={3}>
              <FormattedMessage id="voting.languages" />
            </Text>
            <Spacer size="small" />

            <Text weight="strong" as="p" size={3}>
              {languages.map((language) => language.name).join(", ")}
            </Text>
          </CardPart>
        </Grid>
      </CardPart>
    </MultiplePartsCard>
  );
};
