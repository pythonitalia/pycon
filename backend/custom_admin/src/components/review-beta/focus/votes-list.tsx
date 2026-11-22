import { Badge, Flex, Heading, Separator, Text } from "@radix-ui/themes";
import { CollapsibleCard } from "./collapsible-card";
import type { ReviewProposalFragmentFragment } from "./focus-mode.generated";
import { scoreColor } from "./score-color";
import { SectionLabel } from "./section";

type ScoreOption = { id: string; label: string; numericValue: number };

type Props = {
  votes: ReviewProposalFragmentFragment["votes"];
  scoreOptions: ScoreOption[];
  rankings: ReviewProposalFragmentFragment["rankings"];
};

export const VotesList = ({ votes, scoreOptions, rankings }: Props) => (
  <CollapsibleCard
    summary={
      <Flex gap="2" align="center">
        <Heading as="h3" size="3">
          Votes
        </Heading>
        <Badge color="gray" radius="full">
          {votes.length}
        </Badge>
      </Flex>
    }
  >
    {votes.length === 0 && (
      <Text size="2" color="gray">
        No votes yet.
      </Text>
    )}
    {votes.map((vote) => {
      const optionIndex = scoreOptions.findIndex(
        (option) => option.numericValue === vote.scoreValue,
      );
      return (
        <Flex direction="column" gap="1" key={vote.id}>
          <Flex justify="between" align="center" gap="3">
            <Flex gap="2" align="center">
              <Text size="2" weight="medium">
                {vote.reviewerName}
              </Text>
              {vote.isMine && (
                <Badge size="1" color="gray" variant="outline">
                  You
                </Badge>
              )}
            </Flex>
            <Badge
              size="2"
              color={
                optionIndex === -1
                  ? "gray"
                  : scoreColor(optionIndex, scoreOptions.length)
              }
            >
              {vote.scoreLabel === null
                ? "⊘ No vote"
                : `${vote.scoreLabel} (${vote.scoreValue})`}
            </Badge>
          </Flex>
          {vote.comment && (
            <Text size="2" color="gray" className="whitespace-pre-wrap">
              {vote.comment}
            </Text>
          )}
        </Flex>
      );
    })}
    <Separator size="4" />
    <SectionLabel>Community vote ranking</SectionLabel>
    {rankings.length === 0 ? (
      <Text size="2" color="gray">
        Not generated yet. An admin creates a rank request once community voting
        is over.
      </Text>
    ) : (
      <Flex gap="2" wrap="wrap">
        {rankings.map((ranking) => (
          <Badge key={ranking.tag} size="2" color="gray" variant="surface">
            {ranking.tag}: {ranking.rank} / {ranking.total}
          </Badge>
        ))}
      </Flex>
    )}
  </CollapsibleCard>
);
