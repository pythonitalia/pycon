import { useEffect, useState, useCallback } from "react";

import { useOnBottomScroll } from "./use-on-bottom-scroll";

export const useInfiniteFetchScroll = ({
  fetchMore,
  hasMoreResultsCallback,
  after,
  filters,
}: {
  fetchMore: (variables: any) => any;
  hasMoreResultsCallback: (newData: any) => boolean;
  after?: number;
  filters?: any;
}): {
  isFetchingMore: boolean;
  hasMore: boolean;
  forceLoadMore: () => void;
} => {
  const [isFetchingMore, setIsFetchingMore] = useState(false);
  const [hasMore, setHasMore] = useState(true);

  useEffect(() => {
    setHasMore(true);
  }, [filters]);

  const fetchMoreSubmissionsCallback = useCallback(async () => {
    if (!after || !hasMore || isFetchingMore) {
      return;
    }

    setIsFetchingMore(true);

    const { data: newData } = await fetchMore({
      variables: {
        after: after,
        loadMore: true,
      },
    });
    setIsFetchingMore(false);

    if (!hasMoreResultsCallback(newData)) {
      setHasMore(false);
    }
  }, [after, hasMore, isFetchingMore]);

  useOnBottomScroll(fetchMoreSubmissionsCallback);

  return {
    isFetchingMore,
    hasMore,
    forceLoadMore: () => {
      fetchMoreSubmissionsCallback();
    },
  };
};
