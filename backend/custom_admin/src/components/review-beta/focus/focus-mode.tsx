import { useApolloClient } from "@apollo/client";
import {
  Box,
  Button,
  Callout,
  Flex,
  Link,
  Spinner,
  Text,
} from "@radix-ui/themes";
import { Suspense, useEffect, useState } from "react";
import { createPortal } from "react-dom";
import { useArgs } from "../../shared/args";
import { useNavActionsSlot } from "../nav";
import type { Screen } from "../types";
import {
  NextProposalToReviewDocument,
  type NextProposalToReviewQuery,
  type NextProposalToReviewQueryVariables,
  useFocusReviewSessionSuspenseQuery,
} from "./focus-mode.generated";
import { ProposalReview } from "./proposal-review";
import { TagFilter } from "./tag-filter";
import { readUrlState, writeUrlState } from "./url-state";

export const FocusMode = () => (
  <Suspense fallback={<Loading />}>
    <FocusModeContent />
  </Suspense>
);

const FocusModeContent = () => {
  const { reviewSessionId, screens } = useArgs() as {
    reviewSessionId: number;
    screens: Screen[];
  };
  const client = useApolloClient();
  const {
    data: { reviewSession },
  } = useFocusReviewSessionSuspenseQuery({
    variables: { reviewSessionId: String(reviewSessionId) },
  });

  const navActions = useNavActionsSlot();
  const [initialState] = useState(readUrlState);
  const [excludeTags, setExcludeTags] = useState(initialState.excludeTags);
  const [history, setHistory] = useState<string[]>(
    initialState.proposalId ? [initialState.proposalId] : [],
  );
  const [position, setPosition] = useState(0);
  const [loadingNext, setLoadingNext] = useState(!initialState.proposalId);

  const currentId = history[position] ?? null;
  const shortlistUrl = screens.find((screen) => screen.id === "shortlist")?.url;

  const fetchNext = async (seen: string[]) => {
    setLoadingNext(true);
    const { data } = await client.query<
      NextProposalToReviewQuery,
      NextProposalToReviewQueryVariables
    >({
      query: NextProposalToReviewDocument,
      variables: {
        reviewSessionId: String(reviewSessionId),
        excludeTags,
        seen,
      },
      fetchPolicy: "network-only",
    });
    const nextId = data.nextProposalToReview;
    const newHistory = nextId ? [...seen, nextId] : seen;
    setHistory(newHistory);
    setPosition(nextId ? newHistory.length - 1 : newHistory.length);
    setLoadingNext(false);
  };

  useEffect(() => {
    if (!initialState.proposalId) {
      fetchNext([]);
    }
  }, []);

  useEffect(() => {
    writeUrlState({ proposalId: currentId, excludeTags });
  }, [currentId, excludeTags]);

  const goForward = () => {
    if (position < history.length - 1) {
      setPosition(position + 1);
      return;
    }
    fetchNext(history);
  };

  const goBack = () => setPosition(Math.max(position - 1, 0));

  const [toast, setToast] = useState<string | null>(null);
  useEffect(() => {
    if (!toast) {
      return;
    }
    const timeout = setTimeout(() => setToast(null), 3000);
    return () => clearTimeout(timeout);
  }, [toast]);

  const onVoted = (message: string) => {
    setToast(message);
    goForward();
  };

  if (reviewSession.scoreOptions.length === 0) {
    return (
      <Callout.Root color="amber">
        <Callout.Text>
          This review session has no score options yet. An admin must add them
          in the review session page before anyone can vote.
        </Callout.Text>
      </Callout.Root>
    );
  }

  return (
    <Flex direction="column" gap="4">
      {toast && (
        <Box
          role="status"
          className="fixed left-1/2 top-4 z-50 -translate-x-1/2 rounded-[var(--radius-3)] bg-[var(--color-panel-solid)] shadow-lg"
        >
          <Callout.Root color="green" variant="surface">
            <Callout.Text>✓ {toast}</Callout.Text>
          </Callout.Root>
        </Box>
      )}
      {navActions &&
        createPortal(
          <TagFilter
            tags={reviewSession.tags}
            excluded={excludeTags}
            onChange={setExcludeTags}
          />,
          navActions,
        )}
      {loadingNext && <Loading />}
      {!loadingNext && currentId && (
        <Suspense key={currentId} fallback={<Loading />}>
          <ProposalReview
            key={currentId}
            proposalId={currentId}
            scoreOptions={reviewSession.scoreOptions}
            canGoBack={position > 0}
            onVoted={onVoted}
            onSkip={goForward}
            onBack={goBack}
          />
        </Suspense>
      )}
      {!loadingNext && !currentId && (
        <Flex direction="column" gap="3" align="start">
          <Text size="4" weight="bold">
            You've reviewed everything
          </Text>
          <Flex gap="4">
            {history.length > 0 && (
              <Button variant="soft" color="gray" onClick={goBack}>
                ← Previous
              </Button>
            )}
            {shortlistUrl && (
              <Link href={shortlistUrl}>Go to the Shortlist</Link>
            )}
          </Flex>
        </Flex>
      )}
    </Flex>
  );
};

const Loading = () => (
  <Flex justify="center" py="9">
    <Spinner size="3" />
  </Flex>
);
