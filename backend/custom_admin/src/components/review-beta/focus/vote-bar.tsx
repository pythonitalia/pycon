import {
  Box,
  Button,
  Callout,
  Flex,
  Strong,
  Text,
  TextArea,
} from "@radix-ui/themes";
import { useState } from "react";
import { useArgs } from "../../shared/args";
import {
  type ReviewProposalFragmentFragment,
  useVoteProposalMutation,
} from "./focus-mode.generated";
import { scoreColor } from "./score-color";

const NO_VOTE = "no-vote";

type ScoreOption = { id: string; label: string; numericValue: number };

type Props = {
  proposalId: string;
  proposalTitle: string;
  myVote: ReviewProposalFragmentFragment["myVote"];
  scoreOptions: ScoreOption[];
  canGoBack: boolean;
  onVoted: (message: string) => void;
  onSkip: () => void;
  onBack: () => void;
};

export const VoteBar = ({
  proposalId,
  proposalTitle,
  myVote,
  scoreOptions,
  canGoBack,
  onVoted,
  onSkip,
  onBack,
}: Props) => {
  const { reviewSessionId } = useArgs();
  const [choice, setChoice] = useState<string | null>(
    myVote ? (myVote.scoreOptionId ?? NO_VOTE) : null,
  );
  const [comment, setComment] = useState(myVote?.comment ?? "");
  const [error, setError] = useState<string | null>(null);
  const [voteProposal, { loading }] = useVoteProposalMutation();
  const labelOf = (id: string | null) =>
    id === NO_VOTE
      ? "No vote"
      : scoreOptions.find((option) => option.id === id)?.label;
  const savedLabel = myVote ? labelOf(myVote.scoreOptionId ?? NO_VOTE) : null;

  const vote = async () => {
    setError(null);
    try {
      const { data } = await voteProposal({
        variables: {
          input: {
            reviewSessionId: String(reviewSessionId),
            proposalId,
            scoreOptionId: choice === NO_VOTE ? null : choice,
            comment,
          },
        },
      });
      if (data?.voteProposal.__typename !== "ReviewProposal") {
        setError("This proposal or score option no longer exists.");
        return;
      }
      onVoted(`Saved ${labelOf(choice)} on “${proposalTitle}”`);
    } catch {
      setError("Couldn't save your vote. Try again.");
    }
  };

  return (
    <Box
      className="fixed inset-x-0 bottom-0 z-20 border-t border-[var(--gray-a5)] px-10 py-3 shadow-lg"
      style={{ backgroundColor: "var(--color-panel-solid)" }}
    >
      <Flex direction="column" gap="2">
        <Flex gap="2" wrap="wrap" justify="between" align="center">
          <Flex gap="2" wrap="wrap">
            {scoreOptions.map((option, index) => {
              const picked = option.id === choice;
              return (
                <Button
                  key={option.id}
                  size="2"
                  color={scoreColor(index, scoreOptions.length)}
                  variant={picked ? "solid" : "soft"}
                  aria-pressed={picked}
                  onClick={() => setChoice(option.id)}
                >
                  <span aria-hidden className={picked ? "" : "invisible"}>
                    ✓
                  </span>
                  {option.label} ({option.numericValue})
                </Button>
              );
            })}
            <Button
              size="2"
              color="gray"
              variant={choice === NO_VOTE ? "solid" : "soft"}
              aria-pressed={choice === NO_VOTE}
              onClick={() => setChoice(NO_VOTE)}
              title="Counts as reviewed, not in the score"
            >
              <span
                aria-hidden
                className={choice === NO_VOTE ? "" : "invisible"}
              >
                ✓
              </span>
              ⊘ No vote
            </Button>
          </Flex>
          <Flex gap="2">
            <Button
              variant="soft"
              color="gray"
              disabled={!canGoBack || loading}
              onClick={onBack}
            >
              ← Previous
            </Button>
            <Button
              variant="soft"
              color="gray"
              disabled={loading}
              onClick={onSkip}
            >
              Skip for now
            </Button>
          </Flex>
        </Flex>
        <Flex gap="3" align="center" justify="between">
          <Flex gap="3" align="center" flexGrow="1" minWidth="0">
            <Box flexGrow="1" maxWidth="480px">
              <TextArea
                rows={1}
                placeholder="Comment, visible to the other reviewers"
                value={comment}
                onChange={(e) => setComment(e.target.value)}
                className="[&_textarea]:max-h-40 [&_textarea]:[field-sizing:content]"
                style={{ minHeight: "var(--space-6)" }}
              />
            </Box>
            {savedLabel && (
              <Text size="2" color="gray">
                You voted <Strong>{savedLabel}</Strong>
              </Text>
            )}
          </Flex>
          <Button
            disabled={!choice || loading}
            loading={loading}
            onClick={vote}
          >
            {savedLabel ? "Update vote" : "Vote"} and go to the next
          </Button>
        </Flex>
        {error && (
          <Callout.Root color="red">
            <Callout.Text>{error}</Callout.Text>
          </Callout.Root>
        )}
      </Flex>
    </Box>
  );
};
