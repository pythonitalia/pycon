import {
  MultiplePartsCard,
  CardPart,
  Grid,
  Heading,
  Spacer,
  Text,
  GridColumn,
  InputNumber,
  Link,
} from "@python-italia/pycon-styleguide";
import { ArrowIcon } from "@python-italia/pycon-styleguide/icons";
import React, { useCallback } from "react";
import { FormattedMessage } from "react-intl";

import { SubmissionAccordionFragment, useSendVoteMutation } from "~/types";

type Props = {
  submission: SubmissionAccordionFragment;
};

export const VotingCard = ({
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

      onError(err) {
        console.log(err.message);
      },
    });

  const onSubmitVote = useCallback(
    (value) => {
      if (loading) {
        return;
      }

      const prevVote = submission.myVote ?? { id: `${Math.random()}` };

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
        background="white"
        openLabel={<FormattedMessage id="global.accordion.readMore" />}
        hoverColor="cream"
      >
        <Heading size={4}>{title}</Heading>
      </CardPart>
      <CardPart id="content" contentAlign="left" background="blue">
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
          value={submission?.myVote?.value}
          onClick={onSubmitVote}
        />

        <Text size={3} color="error">
          {error && error.message}
          {submissionData &&
            submissionData.sendVote.__typename === "SendVoteErrors" && (
              <>
                {submissionData.sendVote.nonFieldErrors}{" "}
                {submissionData.sendVote.validationSubmission}{" "}
                {submissionData.sendVote.validationValue}
              </>
            )}
        </Text>
      </CardPart>
      <CardPart id="content" contentAlign="left" background="white" size="none">
        <Grid cols={12} gap="none" divide={true}>
          <GridColumn colSpan={8}>
            <CardPart contentAlign="left" background="white">
              <Text uppercase weight="strong" size="label3">
                <FormattedMessage id="voting.elevatorPitch" />
              </Text>

              <Spacer size="small" />

              <Text as="p" size={2}>
                {elevatorPitch}
              </Text>
            </CardPart>
          </GridColumn>
          <GridColumn colSpan={3}>
            <CardPart contentAlign="left" background="white">
              <Text uppercase weight="strong" size="label3">
                <FormattedMessage id="voting.tags" />
              </Text>
              <Spacer size="small" />

              <Text weight="strong" as="p" size={2}>
                {tags.map((tag) => tag.name).join(", ")}
              </Text>
            </CardPart>
          </GridColumn>
        </Grid>
      </CardPart>

      <CardPart id="content" contentAlign="left" background="white" size="none">
        <Grid cols={12} gap="none" divide={true} equalHeight>
          <GridColumn colSpan={2}>
            <CardPart contentAlign="left" background="white">
              <Text uppercase weight="strong" size="label3">
                <FormattedMessage id="voting.submissionType" />
              </Text>

              <Spacer size="small" />

              <Text as="p" weight="strong" size={2}>
                <FormattedMessage
                  values={{
                    duration: duration.duration,
                    type: submission.type.name,
                  }}
                  id="voting.minutes"
                />
              </Text>
            </CardPart>
          </GridColumn>

          <GridColumn colSpan={2}>
            <CardPart contentAlign="left" background="white">
              <Text uppercase weight="strong" size="label3">
                <FormattedMessage id="voting.audienceLevel" />
              </Text>
              <Spacer size="small" />

              <Text weight="strong" as="p" size={2}>
                {audienceLevel.name}
              </Text>
            </CardPart>
          </GridColumn>
          <GridColumn colSpan={2}>
            <CardPart contentAlign="left" background="white">
              <Text uppercase weight="strong" size="label3">
                <FormattedMessage id="voting.languages" />
              </Text>
              <Spacer size="small" />

              <Text weight="strong" as="p" size={2}>
                {languages.map((language) => language.name).join(", ")}
              </Text>
            </CardPart>
          </GridColumn>
          <GridColumn colSpan={6}>
            <div className="h-full flex items-center justify-end ">
              <Link href={`/submission/${id}`}>
                <CardPart contentAlign="left" background="white">
                  <div className="flex items-center justify-end">
                    <Text size={3} uppercase>
                      <FormattedMessage id="global.accordion.readMore" />
                    </Text>
                    <ArrowIcon />
                  </div>
                </CardPart>
              </Link>
            </div>
          </GridColumn>
        </Grid>
      </CardPart>
    </MultiplePartsCard>
  );
};
