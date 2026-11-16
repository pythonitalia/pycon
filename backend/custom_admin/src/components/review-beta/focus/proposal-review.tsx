import { Button, Callout, Flex, Grid } from "@radix-ui/themes";
import { useArgs } from "../../shared/args";
import { useReviewProposalSuspenseQuery } from "./focus-mode.generated";
import { ProposalPanel } from "./proposal-panel";
import { SpeakerCard } from "./speaker-card";
import { VoteBar } from "./vote-bar";
import { VotesList } from "./votes-list";

type ScoreOption = { id: string; label: string; numericValue: number };

type Props = {
  proposalId: string;
  scoreOptions: ScoreOption[];
  canGoBack: boolean;
  onVoted: (message: string) => void;
  onSkip: () => void;
  onBack: () => void;
};

export const ProposalReview = ({
  proposalId,
  scoreOptions,
  canGoBack,
  onVoted,
  onSkip,
  onBack,
}: Props) => {
  const { reviewSessionId } = useArgs();
  const {
    data: { reviewProposal: proposal },
  } = useReviewProposalSuspenseQuery({
    variables: { reviewSessionId: String(reviewSessionId), proposalId },
    fetchPolicy: "cache-and-network",
  });

  if (!proposal) {
    return (
      <Flex direction="column" gap="3" align="start">
        <Callout.Root color="red">
          <Callout.Text>
            This proposal isn't in this review session, or it was cancelled.
          </Callout.Text>
        </Callout.Root>
        <Flex gap="3">
          {canGoBack && (
            <Button variant="soft" color="gray" onClick={onBack}>
              ← Previous
            </Button>
          )}
          <Button variant="soft" onClick={onSkip}>
            Go to the next proposal
          </Button>
        </Flex>
      </Flex>
    );
  }

  return (
    <Flex direction="column" gap="4" style={{ paddingBottom: 140 }}>
      {proposal.isMine && (
        <Callout.Root color="amber">
          <Callout.Text>This is your proposal. Press No vote.</Callout.Text>
        </Callout.Root>
      )}
      <Grid columns={{ initial: "1", md: "minmax(0, 1fr) 360px" }} gap="5">
        <ProposalPanel proposal={proposal} />
        <Flex direction="column" gap="4">
          <VotesList
            votes={proposal.votes}
            scoreOptions={scoreOptions}
            rankings={proposal.rankings}
          />
          <SpeakerCard speaker={proposal.speaker} />
        </Flex>
      </Grid>
      <VoteBar
        proposalId={proposal.id}
        proposalTitle={proposal.title.en ?? proposal.title.it ?? ""}
        myVote={proposal.myVote}
        scoreOptions={scoreOptions}
        canGoBack={canGoBack}
        onVoted={onVoted}
        onSkip={onSkip}
        onBack={onBack}
      />
    </Flex>
  );
};
